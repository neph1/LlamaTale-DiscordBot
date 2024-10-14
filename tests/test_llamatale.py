from unittest.mock import patch, MagicMock

import sseclient

from llamatale import LlamaTaleInterface
import json

class TestLlamaTaleInterface():
    
    @patch('llamatale_responses.find_image')
    def test_parse_event(self, mock_find_image):
        mock_find_image.return_value = 'image_url'
        config = {
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale',
            'polling_interval': 5,
            'timeout': 10
        }
        llama_tale_interface = LlamaTaleInterface(config)

        mock_push = MagicMock()

        llama_tale_interface.set_push_method(mock_push)

        # Create a mock event
        event = sseclient.Event(event='text')
        event.data = json.dumps({"text": "Hello", "location": "Room", "location_image": "image_url", "npcs": ["some npc"]})

        # Call the parse_event method
        result = llama_tale_interface._parse_event(event)

        mock_push.assert_called_with('Hello', 'http://localhost:8180/tale/static/image_url', 'Room')

    @patch('llamatale_responses.find_image')
    def test_parse_event_with_speaker(self, mock_find_image):
        mock_find_image.return_value = 'speaker.png'
        config = {
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale',
            'polling_interval': 5,
            'timeout': 10
        }
        llama_tale_interface = LlamaTaleInterface(config)

        mock_push = MagicMock()

        llama_tale_interface.last_location = 'Room'
        llama_tale_interface.set_push_method(mock_push)

        event = sseclient.Event(event='text')
        event.data = json.dumps({"text": "Speaker <:> Hello", "location": "Room", "location_image": "image_url", "npcs": ["some npc"]})

        result = llama_tale_interface._parse_event(event)

        mock_push.assert_called_with('Hello', 'http://localhost:8180/tale/static/speaker.png', 'Speaker')
