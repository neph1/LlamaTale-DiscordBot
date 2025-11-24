from unittest.mock import patch, MagicMock

from llamatale import LlamaTaleInterface
import json

class TestLlamaTaleInterface():
    
    @patch('llamatale.threading.Thread')
    @patch('web_utils.find_image')
    def test_parse_message(self, mock_find_image, mock_thread):
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

        # Create a mock WebSocket message
        message = json.dumps({"event": "text", "text": "Hello", "location": "Room", "location_image": "image_url", "npcs": ["some npc"]})

        # Call the parse_message method
        result = llama_tale_interface._parse_message(message)

        mock_push.assert_called()
        args = mock_push.call_args[0]
        assert args[0] == 'Hello'  # text
        assert args[1] == 'image_url'  # image
        assert args[2] == 'Room'  # caption
        assert args[3].text == 'Hello'  # event object

    @patch('llamatale.threading.Thread')
    @patch('web_utils.find_image')
    def test_parse_message_with_speaker(self, mock_find_image, mock_thread):
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

        message = json.dumps({"event": "text", "text": "Speaker <:> Hello", "location": "Room", "location_image": "image_url", "npcs": ["some npc"]})

        result = llama_tale_interface._parse_message(message)

        mock_push.assert_called()
        args = mock_push.call_args[0]
        assert args[0] == 'Hello'  # text
        assert args[1] == 'speaker.png'  # image
        assert args[2] == 'Speaker'  # caption
        assert args[3].speaker == 'Speaker'  # event object
