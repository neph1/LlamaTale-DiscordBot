import asyncio
import discord
from discord.ui import Button, View
import yaml

from bot_utils import format_text
from llamatale import LlamaTaleInterface


class GameActionView(View):
    """Discord View containing buttons for exits and items."""
    
    def __init__(self, llama_tale: LlamaTaleInterface, exits: list, items: list):
        super().__init__(timeout=None)  # No timeout for game actions
        self.llama_tale = llama_tale
        
        # Add exit buttons (up to 5 to stay within Discord's limits)
        for exit_name in exits[:5]:
            button = Button(label=f"🚪 {exit_name}", style=discord.ButtonStyle.primary, custom_id=f"exit_{exit_name}")
            button.callback = self._create_exit_callback(exit_name)
            self.add_item(button)
        
        # Add item buttons (up to remaining slots, max 25 total components)
        remaining_slots = 25 - len(self.children)
        for item_name in items[:min(remaining_slots, 5)]:
            button = Button(label=f"📦 {item_name}", style=discord.ButtonStyle.success, custom_id=f"item_{item_name}")
            button.callback = self._create_item_callback(item_name)
            self.add_item(button)
    
    def _create_exit_callback(self, exit_name: str):
        """Create a callback for exit button."""
        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(f"Moving to: {exit_name}", ephemeral=True)
            self.llama_tale.call(exit_name)
        return callback
    
    def _create_item_callback(self, item_name: str):
        """Create a callback for item button."""
        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(f"Taking: {item_name}", ephemeral=True)
            self.llama_tale.call(f"take {item_name}")
        return callback


class DiscordBot(discord.Client):

    def __init__(self, intents, config):
        super().__init__(intents=intents)
        self.channel = None
        self.llama_tale = LlamaTaleInterface(config=config)
        self.last_message = None
        self.last_image = None
        self.last_caption = None
        self.last_event = None
        

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
                self.push(self.last_message, self.last_image, self.last_caption, self.last_event)
                return
            elif message.content == 'help':
                await message.channel.send('Commands: start (start listening to LlamaTale), remind me (show last message), help (show this message)')

            prompt = message.content
            response = self.llama_tale.call(prompt=prompt)

            if response:
                self._output(response, message)

    def push(self, server_message, image, caption, event=None):
        if not self.channel:
            print('No channel to send message to.')
            return
        if image:
            client.loop.create_task(self._send_image(image, caption, self.channel))
        client.loop.create_task(self._output(server_message, self.channel, event))
        self.last_message = server_message
        self.last_image = image
        self.last_caption = caption
        self.last_event = event

    async def _output(self, server_message, channel: discord.GroupChannel, event=None):
        # Create an embed if we have structured event data with exits or items
        if event and (event.exits or event.items):
            embed = discord.Embed(description=format_text(server_message), color=discord.Color.blue())
            
            # Add exits field
            if event.exits:
                exits_text = ", ".join(event.exits)
                embed.add_field(name="🚪 Exits", value=exits_text, inline=False)
            
            # Add items field
            if event.items:
                items_text = ", ".join(event.items)
                embed.add_field(name="📦 Items", value=items_text, inline=False)
            
            # Add NPCs field
            if event.npcs:
                npcs_text = ", ".join(event.npcs)
                embed.add_field(name="👥 NPCs", value=npcs_text, inline=False)
            
            # Create view with buttons
            view = GameActionView(self.llama_tale, event.exits, event.items)
            
            await channel.send(embed=embed, view=view)
        else:
            # Fall back to regular text output
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

