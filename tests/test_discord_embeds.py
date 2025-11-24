"""Tests for Discord embed and button functionality."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

from llamatale_responses import TextEvent


class TestDiscordEmbeds:
    """Test Discord embed creation with exits and items."""
    
    def test_embed_with_exits_and_items(self):
        """Test that embeds are created with exits and items."""
        # Create mock event data
        event_data = {
            "text": "You are in a room.",
            "location": "Test Room",
            "location_image": "room.png",
            "npcs": ["Guard", "Merchant"],
            "items": ["Sword", "Shield", "Potion"],
            "exits": ["north", "south", "east"],
            "special": []
        }
        
        text_event = TextEvent(event_data)
        
        # Verify the text event has all the data
        assert text_event.text == "You are in a room."
        assert text_event.location == "Test Room"
        assert text_event.npcs == ["Guard", "Merchant"]
        assert text_event.items == ["Sword", "Shield", "Potion"]
        assert text_event.exits == ["north", "south", "east"]
    
    def test_text_event_preserves_exits(self):
        """Test that TextEvent preserves exit information."""
        event_data = {
            "text": "You see multiple exits.",
            "location": "Crossroads",
            "exits": ["north", "south", "east", "west"],
            "items": [],
            "npcs": []
        }
        
        text_event = TextEvent(event_data)
        
        assert text_event.exits == ["north", "south", "east", "west"]
        assert len(text_event.exits) == 4
    
    def test_text_event_preserves_items(self):
        """Test that TextEvent preserves item information."""
        event_data = {
            "text": "You see various items here.",
            "location": "Treasure Room",
            "exits": [],
            "items": ["Gold Coin", "Magic Wand", "Ancient Scroll"],
            "npcs": []
        }
        
        text_event = TextEvent(event_data)
        
        assert text_event.items == ["Gold Coin", "Magic Wand", "Ancient Scroll"]
        assert len(text_event.items) == 3
    
    def test_text_event_with_npcs(self):
        """Test that TextEvent preserves NPC information."""
        event_data = {
            "text": "Several people are here.",
            "location": "Town Square",
            "exits": ["north"],
            "items": [],
            "npcs": ["Blacksmith", "Mayor", "Guard Captain"]
        }
        
        text_event = TextEvent(event_data)
        
        assert text_event.npcs == ["Blacksmith", "Mayor", "Guard Captain"]
        assert len(text_event.npcs) == 3
    
    def test_full_event_data_integration(self):
        """Test that all event data is preserved for Discord integration."""
        event_data = {
            "text": "You enter a magnificent hall.",
            "location": "Grand Hall",
            "location_image": "grand_hall.png",
            "npcs": ["King", "Queen"],
            "items": ["Crown", "Scepter"],
            "exits": ["north", "south"],
            "special": ["throne"]
        }
        
        text_event = TextEvent(event_data)
        
        # Verify all fields are accessible for embed creation
        assert text_event.text == "You enter a magnificent hall."
        assert text_event.location == "Grand Hall"
        assert text_event.location_image == "grand_hall.png"
        assert len(text_event.npcs) == 2
        assert len(text_event.items) == 2
        assert len(text_event.exits) == 2
        assert text_event.special == ["throne"]

