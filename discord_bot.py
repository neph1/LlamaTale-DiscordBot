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
        self.last_message = None
        self.last_image = None
        self.last_caption = None
        

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
            elif message.content == 'remind me':
                self.push(self.last_message, self.last_image, self.last_caption)
                return
            elif message.content == 'help':
                await message.channel.send('Commands: start (start listening to LlamaTale), remind me (show last message), help (show this message)')

            prompt = message.content
            response = self.llama_tale.call(prompt=prompt)

            if response:
                self._output(response, message)

    def push(self, server_message, image, caption):
        if not self.channel:
            print('No channel to send message to.')
            return
        if image:
            client.loop.create_task(self._send_image(image, caption, self.channel))
        client.loop.create_task(self._output(server_message, self.channel))
        self.last_message = server_message
        self.last_image = image
        self.last_caption = caption

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
            embed = discord.Embed(title=caption)
            embed.set_image(url=f'attachment://{image_path}')
            if image_path.startswith('http'):
                await channel.send(embed=embed)
            else:
                file = discord.File(image_path)
                await channel.send(file = file, embed=embed)
        except Exception as e:
            print(f"Error: {e}")

intents = discord.Intents.default()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

TOKEN = config['DISCORD_TOKEN']
GUILD = config['DISCORD_SERVER']

client = DiscordBot(intents=intents, config=config)
client.run(TOKEN)

