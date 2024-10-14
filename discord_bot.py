import discord
import yaml

from bot_utils import format_text
from llamatale import LLamaTaleInterface


class DiscordBot(discord.Client):

    def __init__(self, intents, config):
        super().__init__(intents=intents)
        
        self.llama_tale = LLamaTaleInterface(config=config)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member: discord.Member):
        pass
        
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.channel.type == discord.ChannelType.private:
            self.channel = message.channel

            if message.content == 'ping':
                await message.channel.send('pong')
            elif message.content == 'start':
                self.channel = message.channel
                self.llama_tale.start_sse_listener()

            prompt = message.content
            response = self.llama_tale.call(prompt=prompt)

            if response:
                self._output(response, message)
            else:
                print('Something went wrong. No response to send')

    def push(self, server_message, image, caption):
        self._output(server_message, self.channel)
        if image:
            self._send_image(image, caption, self.channel)

    async def _output(self, server_message, channel: discord.Channel):
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

    async def _send_image(self, image_path, caption, channel: discord.Channel):
        with open(image_path, "rb") as image_file:
            await channel.send(file=discord.File(image_file), content=caption)

intents = discord.Intents.default()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

TOKEN = config['DISCORD_TOKEN']
GUILD = config['DISCORD_SERVER']

client = DiscordBot(intents=intents, config=config)
client.run(TOKEN)

