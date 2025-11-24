import json
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
        text_event = TextEvent(event_data)

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
        text_event = TextEvent(event_data)

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
        text_event = TextEvent(event_data)

        assert text_event.speaker == "Speaker"
        assert text_event.text == "Hello World"
        assert text_event.speaker_image == "speaker"  # Base name without extension

    def test_text_event_missing_fields(self):
        event_data = {
            "text": "Hello World"
        }
        text_event = TextEvent(event_data)

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
        text_event = TextEvent(event_data)

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
        text_event = TextEvent(event_data)

        # Whitespace should be stripped
        assert text_event.npcs == ["giant rat", "giant rat"]
        assert text_event.items == ["breast_plate", "sword"]
        assert text_event.exits == ["north", "south"]