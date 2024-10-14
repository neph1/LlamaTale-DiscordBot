import asyncio
import discord
import yaml

from bot_utils import format_text
from llamatale import LlamaTaleInterface


class DiscordBot(discord.Client):

    def __init__(self, intents, config):
        super().__init__(intents=intents)
        self.channel = None
        self.llama_tale = LlamaTaleInterface(config=config)
        

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member: discord.Member):
        pass
        
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            if message.content == 'ping':
                await message.channel.send('pong')
            elif not self.channel and message.content == 'start':
                self.channel = message.channel
                self.llama_tale.set_push_method(self.push)
                return

            prompt = message.content
            response = self.llama_tale.call(prompt=prompt)

            if response:
                self._output(response, message)

    def push(self, server_message, image, caption):
        if not self.channel:
            print('No channel to send message to.')
            return
        print(server_message, image, caption)
        client.loop.create_task(self._output(server_message, self.channel))
        if image:
            client.loop.create_task(self._send_image(image, caption, self.channel))

    async def _output(self, server_message, channel: discord.GroupChannel):
        response_lines = server_message.split('\n\n')
        output = ''
        for line in response_lines:
            if len(output) + len(line) < 2000:
                output += line
            else:
                await channel.send(format_text(output))
                output = line
        if output:
            await channel.send(format_text(output))

    async def _send_image(self, image_path, caption, channel: discord.GroupChannel):
        try:
            with open(image_path, "rb") as image_file:
                await channel.send(file=discord.File(image_file), content=caption)
        except Exception as e:
            print(f"Error: {e}")

intents = discord.Intents.default()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

TOKEN = config['DISCORD_TOKEN']
GUILD = config['DISCORD_SERVER']

client = DiscordBot(intents=intents, config=config)
client.run(TOKEN)

