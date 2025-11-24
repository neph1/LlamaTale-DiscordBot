
import json
import re

from web_utils import find_image
import web_utils

dialogue_separator = ' <:> '

class ServerSentEvent:
    def __init__(self, data):
        pass


class TextEvent(ServerSentEvent):
    def __init__(self, data):
        # Handle both dict (from WebSocket) and sseclient.Event (for backwards compatibility)
        if isinstance(data, dict):
            event_data = data
        else:
            # Legacy SSE format
            event_data = json.loads(data.data)
        
        self.text = event_data.get('text', None)
        self.location = event_data.get('location', None)
        self.location_image = event_data.get('location_image', None) if self.location else None
        
        # Handle npcs, items, exits - they can be either strings (comma-separated) or lists
        self.npcs = self._parse_list_field(event_data.get('npcs', []))
        self.items = self._parse_list_field(event_data.get('items', []))
        self.exits = self._parse_list_field(event_data.get('exits', []))
        self.special = self._parse_list_field(event_data.get('special', []))
        
        if dialogue_separator in self.text:
            self.speaker, self.text = web_utils.split_text(self.text)
            self.speaker_image = self.speaker.lower().replace(' ', '_')
        else:
            self.speaker = None
            self.speaker_image = None
        self.text = re.sub('<[^<]+?>', '', self.text)
    
    def _parse_list_field(self, field):
        """Parse a field that can be either a string (comma-separated) or a list."""
        if isinstance(field, str):
            # If it's a string, split by comma and strip whitespace
            return [item.strip() for item in field.split(',') if item.strip()]
        elif isinstance(field, list):
            # If it's already a list, return as-is
            return field
        else:
            # If it's something else, return empty list
            return []

class ErrorEvent(ServerSentEvent):
    def __init__(self, event):
        self.text = 'An error has occurred.'

class MessageEvent(ServerSentEvent):
    def __init__(self, event):
        pass

