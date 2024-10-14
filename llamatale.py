import asyncio
from extension import ExtensionInterface
import threading
import requests
import sseclient

from llamatale_responses import TextEvent


class LlamaTaleInterface(ExtensionInterface):

    def __init__(self, config):
        self.config = config
        self.port = self.config.get('port', 8180)
        self.host = self.config.get('url', f'http://localhost')
        endpoint = self.config.get('endpoint', '/tale')
        self.url = f"{self.host}:{self.port}{endpoint}/eventsource"
        self.polling_interval = self.config.get('polling_interval', 5)
        self.timeout = self.config.get('timeout', 10)
        self.game_state = None
        self.last_location = None
        self.resources_path = f"{self.host}:{self.port}{endpoint}/static/"
        

    def check_for_trigger(self, prompt: str) -> bool:
        return True

    def call(self, prompt):

        encoded_cmd = f"cmd={prompt}\n\n"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        
        response = requests.post(f"{self.host}:{self.port}/tale/input", data=encoded_cmd, headers=headers)
        if not response.ok:
            print(f"Error: {response.status_code}")
            return
        return

    def _start_sse_listener(self):
        self.sse_thread = threading.Thread(target=self._listen_to_sse)
        self.sse_thread.daemon = True  # Set as a daemon thread to terminate with the main program
        self.sse_thread.start()

    def _listen_to_sse(self):
        print("Listening to SSE events at", self.url)
        response = requests.get(f"{self.host}:{self.port}/tale/story", stream=True)
        try:
            headers = {
                'Connection': 'keep-alive',
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache',
            }

            response = requests.get(self.url, stream=True, headers=headers)
            response.raise_for_status()
            
            client = sseclient.SSEClient(response)

            for event in client.events():
                self._parse_event(event)

        except Exception as e:
            print(f"Error: {e}")

    def _parse_event(self, event: sseclient.Event):
        print(f"Received event: {event.data}")
        if event.event == "text":
            response = TextEvent(event)
            image = None
            caption = None
            if response.location != self.last_location:
                self.last_location = response.location
                image = self.resources_path + response.location_image
                caption = response.location
            elif response.speaker:
                image = self.resources_path + response.speaker_image
                caption = response.speaker
            if self.push:
                self.push(response.text, image, caption)


    def set_push_method(self, push: callable):
        self.push = push
        self._start_sse_listener()
