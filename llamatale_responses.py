
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
        self.npcs = data.get('npcs', [])
        self.items = data.get('items', [])
        self.exits = data.get('exits', [])
        self.special = data.get('special', [])
        if dialogue_separator in self.text:
            self.speaker, self.text = web_utils.split_text(self.text)
            self.speaker_image = self.speaker.lower().replace(' ', '_')
        else:
            self.speaker = None
            self.speaker_image = None
        self.text = re.sub('<[^<]+?>', '', self.text)

class ErrorEvent(ServerSentEvent):
    def __init__(self, event):
        self.text = 'An error has occurred.'

class MessageEvent(ServerSentEvent):
    def __init__(self, event):
        pass

