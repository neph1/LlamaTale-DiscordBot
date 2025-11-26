
import json
import re

import sseclient

from web_utils import find_image
import web_utils

dialogue_separator = ' <:> '

class ServerSentEvent:
    def __init__(self, event):
        pass


class TextEvent(ServerSentEvent):
    def __init__(self, event: sseclient.Event):
        data = json.loads(event.data)
        self.text = data.get('text', None)
        self.location = data.get('location', None)
        self.location_image = data.get('location_image', None) if self.location else None
        
        # Handle npcs, items, exits - they can be either strings (comma-separated) or lists
        self.npcs = self._parse_list_field(data.get('npcs', []))
        self.items = self._parse_list_field(data.get('items', []))
        self.exits = self._parse_list_field(data.get('exits', []))
        self.special = self._parse_list_field(data.get('special', []))
        
        # Handle optional image data for items and NPCs (sent by server)
        self.item_images = self._parse_list_field(data.get('item_images', []))
        self.npc_images = self._parse_list_field(data.get('npc_images', []))
        
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
    
    def get_item_image(self, item_name: str) -> str:
        """Get the image name for a specific item by name.
        
        Returns the image name if found, or derives one from the item name.
        """
        # Try to find exact match by index
        try:
            index = self.items.index(item_name)
            if index < len(self.item_images) and self.item_images[index]:
                return self.item_images[index]
        except (ValueError, IndexError):
            pass
        
        # Fallback: derive from item name (lowercase, underscores for spaces)
        return item_name.lower().replace(' ', '_')
    
    def get_npc_image(self, npc_name: str) -> str:
        """Get the image name for a specific NPC by name.
        
        Returns the image name if found, or derives one from the NPC name.
        """
        # Try to find exact match by index
        try:
            index = self.npcs.index(npc_name)
            if index < len(self.npc_images) and self.npc_images[index]:
                return self.npc_images[index]
        except (ValueError, IndexError):
            pass
        
        # Fallback: derive from NPC name (lowercase, underscores for spaces)
        return npc_name.lower().replace(' ', '_')

class ErrorEvent(ServerSentEvent):
    def __init__(self, event):
        self.text = 'An error has occurred.'

class MessageEvent(ServerSentEvent):
    def __init__(self, event):
        pass

