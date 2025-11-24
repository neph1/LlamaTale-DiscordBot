import asyncio
from extension import ExtensionInterface
import threading
import requests
import websockets
import json

from llamatale_responses import TextEvent
import web_utils


class LlamaTaleInterface(ExtensionInterface):

    def __init__(self, config):
        self.config = config
        self.port = self.config.get('port', 8180)
        self.host = self.config.get('url', f'http://localhost')
        endpoint = self.config.get('endpoint', '/tale')
        # Convert http/https to ws/wss for WebSocket connection
        ws_host = self.host.replace('http://', 'ws://').replace('https://', 'wss://')
        self.url = f"{ws_host}:{self.port}{endpoint}/ws"
        self.polling_interval = self.config.get('polling_interval', 5)
        self.timeout = self.config.get('timeout', 10)
        self.game_state = None
        self.last_location = None
        if config.get('llama_tale_path', None):
            self.resources_path = config['llama_tale_path']
        else:
            self.resources_path = f"{self.host}:{self.port}{endpoint}/static/resources/"
        

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

    def _start_ws_listener(self):
        self.ws_thread = threading.Thread(target=self._listen_to_ws)
        self.ws_thread.daemon = True  # Set as a daemon thread to terminate with the main program
        self.ws_thread.start()

    def _listen_to_ws(self):
        print("Listening to WebSocket events at", self.url)
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._ws_client())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            loop.close()

    async def _ws_client(self):
        try:
            async with websockets.connect(self.url) as websocket:
                async for message in websocket:
                    self._parse_message(message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Attempting to reconnect...")
            # Simple reconnection attempt
            try:
                await asyncio.sleep(2)
                await self._ws_client()
            except Exception as e:
                print(f"Reconnection failed: {e}")
        except Exception as e:
            print(f"WebSocket error: {e}")

    def _parse_message(self, message: str):
        try:
            data = json.loads(message)
            event_type = data.get('event', 'text')
            if event_type == "text":
                response = TextEvent(data)
                image = None
                caption = None
                if response.location != self.last_location:
                    self.last_location = response.location
                    image = web_utils.find_image(response.location_image, self.resources_path)
                    caption = response.location
                elif response.speaker:
                    if response.speaker_image:
                        image = web_utils.find_image(response.speaker_image, self.resources_path)
                    caption = response.speaker
                if self.push:
                    self.push(response.text, image, caption, response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse WebSocket message: {e}")


    def set_push_method(self, push: callable):
        self.push = push
        self._start_ws_listener()
