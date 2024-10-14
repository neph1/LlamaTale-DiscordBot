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
        assert text_event.speaker_image == "speaker.png"

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