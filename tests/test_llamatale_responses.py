import json
import sseclient
from llamatale_responses import TextEvent, dialogue_separator
from unittest.mock import patch



class TestLlamaTaleResponses:


    @patch('llamatale_responses.find_image')
    def test_text_event_initialization(self, mock_find_image):
        mock_find_image.return_value = 'room1.png'
        event_data = {
            "text": "Hello World",
            "location": "Room 1",
            "location_image": "room1.png",
            "npcs": ["NPC1", "NPC2"],
            "items": ["Item1", "Item2"],
            "exits": ["Exit1", "Exit2"],
            "special": ["Special1"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.text == "Hello World"
        assert text_event.location == "Room 1"
        assert text_event.location_image == "room1.png"
        assert text_event.npcs == ["NPC1", "NPC2"]
        assert text_event.items == ["Item1", "Item2"]
        assert text_event.exits == ["Exit1", "Exit2"]
        assert text_event.special == ["Special1"]

    def test_text_event_with_html_tags(self):
        event_data = {
            "text": "<p>Hello <b>World</b></p>",
            "location": "Room 1",
            "location_image": "room1.png",
            "npcs": ["NPC1", "NPC2"],
            "items": ["Item1", "Item2"],
            "exits": ["Exit1", "Exit2"],
            "special": ["Special1"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.text == "Hello World"

    @patch('llamatale_responses.find_image')
    def test_text_event_with_dialogue_separator(self, mock_find_image):
        mock_find_image.side_effect = ['room1.png', 'speaker.png']
        event_data = {
            "text": f"Speaker{dialogue_separator}Hello World",
            "location": "Room 1",
            "location_image": "room1.png",
            "npcs": ["NPC1", "NPC2"],
            "items": ["Item1", "Item2"],
            "exits": ["Exit1", "Exit2"],
            "special": ["Special1"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.speaker == "Speaker"
        assert text_event.text == "Hello World"
        assert text_event.speaker_image == "speaker"  # Base name without extension

    def test_text_event_missing_fields(self):
        event_data = {
            "text": "Hello World"
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.text == "Hello World"
        assert text_event.location is None
        assert text_event.location_image is None
        assert text_event.npcs == []
        assert text_event.items == []
        assert text_event.exits == []
        assert text_event.special == []

    def test_text_event_with_string_npcs_and_items(self):
        """Test parsing when npcs and items come as comma-separated strings."""
        event_data = {
            "text": "You see some creatures and items here.",
            "location": "Test Room",
            "npcs": "giant rat,giant rat",
            "items": "breast_plate,sword",
            "exits": "north,south,east",
            "special": ""
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.text == "You see some creatures and items here."
        assert text_event.npcs == ["giant rat", "giant rat"]
        assert text_event.items == ["breast_plate", "sword"]
        assert text_event.exits == ["north", "south", "east"]
        assert text_event.special == []

    def test_text_event_with_string_whitespace(self):
        """Test parsing handles whitespace in comma-separated strings."""
        event_data = {
            "text": "Test",
            "npcs": " giant rat , giant rat ",
            "items": " breast_plate , sword ",
            "exits": " north , south ",
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        # Whitespace should be stripped
        assert text_event.npcs == ["giant rat", "giant rat"]
        assert text_event.items == ["breast_plate", "sword"]
        assert text_event.exits == ["north", "south"]

    def test_text_event_with_item_images(self):
        """Test parsing item_images from server data."""
        event_data = {
            "text": "You see some items here.",
            "location": "Test Room",
            "items": ["Sword", "Shield", "Potion"],
            "item_images": ["sword_icon", "shield_icon", "potion_icon"],
            "npcs": [],
            "exits": []
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.items == ["Sword", "Shield", "Potion"]
        assert text_event.item_images == ["sword_icon", "shield_icon", "potion_icon"]

    def test_text_event_with_npc_images(self):
        """Test parsing npc_images from server data."""
        event_data = {
            "text": "You see some NPCs here.",
            "location": "Test Room",
            "npcs": ["Guard", "Merchant", "Wizard"],
            "npc_images": ["guard_portrait", "merchant_portrait", "wizard_portrait"],
            "items": [],
            "exits": []
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.npcs == ["Guard", "Merchant", "Wizard"]
        assert text_event.npc_images == ["guard_portrait", "merchant_portrait", "wizard_portrait"]

    def test_text_event_without_image_arrays(self):
        """Test that item_images and npc_images default to empty arrays."""
        event_data = {
            "text": "You see some things here.",
            "location": "Test Room",
            "npcs": ["Guard"],
            "items": ["Sword"],
            "exits": []
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.item_images == []
        assert text_event.npc_images == []

    def test_get_item_image_with_explicit_images(self):
        """Test getting item image when explicitly provided by server."""
        event_data = {
            "text": "Items here.",
            "items": ["Sword", "Shield", "Potion"],
            "item_images": ["sword_icon", "shield_icon", "potion_icon"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.get_item_image("Sword") == "sword_icon"
        assert text_event.get_item_image("Shield") == "shield_icon"
        assert text_event.get_item_image("Potion") == "potion_icon"

    def test_get_item_image_with_fallback(self):
        """Test getting item image falls back to derived name."""
        event_data = {
            "text": "Items here.",
            "items": ["Magic Sword", "Ancient Shield"],
            "item_images": []
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.get_item_image("Magic Sword") == "magic_sword"
        assert text_event.get_item_image("Ancient Shield") == "ancient_shield"

    def test_get_npc_image_with_explicit_images(self):
        """Test getting NPC image when explicitly provided by server."""
        event_data = {
            "text": "NPCs here.",
            "npcs": ["Guard Captain", "Merchant", "Wizard"],
            "npc_images": ["captain_portrait", "merchant_portrait", "wizard_portrait"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.get_npc_image("Guard Captain") == "captain_portrait"
        assert text_event.get_npc_image("Merchant") == "merchant_portrait"
        assert text_event.get_npc_image("Wizard") == "wizard_portrait"

    def test_get_npc_image_with_fallback(self):
        """Test getting NPC image falls back to derived name."""
        event_data = {
            "text": "NPCs here.",
            "npcs": ["Guard Captain", "Old Merchant"],
            "npc_images": []
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        assert text_event.get_npc_image("Guard Captain") == "guard_captain"
        assert text_event.get_npc_image("Old Merchant") == "old_merchant"

    def test_get_item_image_not_in_list(self):
        """Test getting item image for item not in the list."""
        event_data = {
            "text": "Items here.",
            "items": ["Sword"],
            "item_images": ["sword_icon"]
        }
        event = sseclient.Event(data=json.dumps(event_data))
        text_event = TextEvent(event)

        # Should fallback to derived name
        assert text_event.get_item_image("Unknown Item") == "unknown_item"