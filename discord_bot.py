import asyncio
import discord
from discord import app_commands
from discord.ui import Button, View
import yaml

from bot_utils import format_text
from llamatale import LlamaTaleInterface


class GameActionView(View):
    """Discord View containing buttons for exits and items."""
    
    def __init__(self, llama_tale: LlamaTaleInterface, exits: list, items: list):
        super().__init__(timeout=300)  # 5 minute timeout for game actions
        self.llama_tale = llama_tale
        
        # Add exit buttons (up to 5 to stay within Discord's limits)
        for i, exit_name in enumerate(exits[:5]):
            # Use index-based custom_id to avoid issues with special characters
            button = Button(label=f"🚪 {exit_name}", style=discord.ButtonStyle.primary, custom_id=f"exit_{i}")
            button.callback = self._create_exit_callback(exit_name)
            self.add_item(button)
        
        # Add item buttons (up to remaining slots, max 25 total components)
        remaining_slots = 25 - len(self.children)
        for i, item_name in enumerate(items[:min(remaining_slots, 5)]):
            # Use index-based custom_id to avoid issues with special characters
            button = Button(label=f"📦 {item_name}", style=discord.ButtonStyle.success, custom_id=f"item_{i}")
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
        self.tree = app_commands.CommandTree(self)
        self.channel = None
        self.llama_tale = LlamaTaleInterface(config=config)
        self.last_message = None
        self.last_image = None
        self.last_caption = None
        self.last_event = None
        self.last_command = None  # Track the last command for context-aware image display
        self._setup_commands()
        

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        # Sync slash commands with Discord
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def _check_channel(self, interaction: discord.Interaction) -> bool:
        """Check if channel is set and respond with error if not."""
        if not self.channel:
            await interaction.response.send_message("Please start the game first with 'start' in DM.", ephemeral=True)
            return False
        return True

    def _setup_commands(self):
        """Set up all slash commands for the bot."""
        
        @self.tree.command(name="look", description="Look around your current location")
        async def look(interaction: discord.Interaction):
            """Look around the current location."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Looking around...", ephemeral=True)
            self.llama_tale.call("look")
        
        @self.tree.command(name="say", description="Say something in the game")
        async def say(interaction: discord.Interaction, message: str):
            """Say something in the game."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Saying: {message}", ephemeral=True)
            self.llama_tale.call(f"say {message}")
        
        @self.tree.command(name="take", description="Take an item")
        async def take(interaction: discord.Interaction, item: str):
            """Take an item from the current location."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Taking: {item}", ephemeral=True)
            self.llama_tale.call(f"take {item}")
        
        @self.tree.command(name="attack", description="Attack a target")
        async def attack(interaction: discord.Interaction, target: str):
            """Attack a target."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Attacking: {target}", ephemeral=True)
            self.llama_tale.call(f"attack {target}")
        
        @self.tree.command(name="north", description="Go north")
        async def north(interaction: discord.Interaction):
            """Move north."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Moving north...", ephemeral=True)
            self.llama_tale.call("north")
        
        @self.tree.command(name="south", description="Go south")
        async def south(interaction: discord.Interaction):
            """Move south."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Moving south...", ephemeral=True)
            self.llama_tale.call("south")
        
        @self.tree.command(name="east", description="Go east")
        async def east(interaction: discord.Interaction):
            """Move east."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Moving east...", ephemeral=True)
            self.llama_tale.call("east")
        
        @self.tree.command(name="west", description="Go west")
        async def west(interaction: discord.Interaction):
            """Move west."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Moving west...", ephemeral=True)
            self.llama_tale.call("west")
        
        @self.tree.command(name="loot", description="Loot a target or container")
        async def loot(interaction: discord.Interaction, target: str):
            """Loot a target or container."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Looting: {target}", ephemeral=True)
            self.llama_tale.call(f"loot {target}")
        
        @self.tree.command(name="wear", description="Wear an item")
        async def wear(interaction: discord.Interaction, item: str):
            """Wear an item."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Wearing: {item}", ephemeral=True)
            self.llama_tale.call(f"wear {item}")
        
        @self.tree.command(name="wield", description="Wield a weapon")
        async def wield(interaction: discord.Interaction, weapon: str):
            """Wield a weapon."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Wielding: {weapon}", ephemeral=True)
            self.llama_tale.call(f"wield {weapon}")
        
        @self.tree.command(name="drop", description="Drop an item")
        async def drop(interaction: discord.Interaction, item: str):
            """Drop an item from your inventory."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Dropping: {item}", ephemeral=True)
            self.llama_tale.call(f"drop {item}")
        
        @self.tree.command(name="examine", description="Examine an object or creature")
        async def examine(interaction: discord.Interaction, target: str):
            """Examine an object or creature."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Examining: {target}", ephemeral=True)
            self.last_command = f"examine {target}"
            self.llama_tale.call(f"examine {target}")
        
        @self.tree.command(name="open", description="Open a door or container")
        async def open_cmd(interaction: discord.Interaction, target: str):
            """Open a door or container."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Opening: {target}", ephemeral=True)
            self.llama_tale.call(f"open {target}")
        
        @self.tree.command(name="close", description="Close a door or container")
        async def close(interaction: discord.Interaction, target: str):
            """Close a door or container."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Closing: {target}", ephemeral=True)
            self.llama_tale.call(f"close {target}")
        
        @self.tree.command(name="use", description="Use an item")
        async def use(interaction: discord.Interaction, item: str, target: str = ""):
            """Use an item, optionally on a target."""
            if not await self._check_channel(interaction):
                return
            if target:
                await interaction.response.send_message(f"Using {item} on {target}", ephemeral=True)
                self.llama_tale.call(f"use {item} {target}")
            else:
                await interaction.response.send_message(f"Using: {item}", ephemeral=True)
                self.llama_tale.call(f"use {item}")
        
        @self.tree.command(name="inventory", description="Check your inventory")
        async def inventory(interaction: discord.Interaction):
            """Check your inventory."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message("Checking inventory...", ephemeral=True)
            self.llama_tale.call("inventory")
        
        @self.tree.command(name="help", description="Show available commands")
        async def help_cmd(interaction: discord.Interaction):
            """Show available commands."""
            help_text = """
**LlamaTale Discord Bot Commands:**

**Movement:**
• `/north`, `/south`, `/east`, `/west` - Move in cardinal directions

**Actions:**
• `/look` - Look around your current location
• `/take <item>` - Take an item
• `/drop <item>` - Drop an item
• `/examine <target>` - Examine something
• `/inventory` - Check your inventory

**Combat:**
• `/attack <target>` - Attack a target
• `/loot <target>` - Loot a target or container

**Equipment:**
• `/wear <item>` - Wear an item
• `/wield <weapon>` - Wield a weapon

**Interaction:**
• `/say <message>` - Say something
• `/give <item> <target>` - Give an item to someone
• `/use <item> [target]` - Use an item
• `/open <target>` - Open a door or container
• `/close <target>` - Close a door or container

You can also type commands directly in the chat (e.g., "look", "go north", etc.)
            """
            await interaction.response.send_message(help_text, ephemeral=True)
        
        @self.tree.command(name="give", description="Give an item to someone")
        async def give(interaction: discord.Interaction, item: str, target: str):
            """Give an item to a target."""
            if not await self._check_channel(interaction):
                return
            await interaction.response.send_message(f"Giving {item} to {target}", ephemeral=True)
            self.llama_tale.call(f"give {item} {target}")

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
            self.last_command = prompt  # Track the command for context-aware image display
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
        # Detect if we're examining an item or NPC to show its thumbnail
        thumbnail_path = None
        if event and self.last_command and self.last_command.startswith('examine '):
            target = self.last_command[8:].strip()  # Extract the target from "examine <target>"
            
            # Check if target is an item
            if target in event.items:
                image_name = event.get_item_image(target)
                from web_utils import find_image
                thumbnail_path = find_image(image_name, self.llama_tale.resources_path)
            # Check if target is an NPC
            elif target in event.npcs:
                image_name = event.get_npc_image(target)
                from web_utils import find_image
                thumbnail_path = find_image(image_name, self.llama_tale.resources_path)
        
        # Create an embed if we have structured event data with exits or items
        if event and (event.exits or event.items or thumbnail_path):
            embed = discord.Embed(description=format_text(server_message), color=discord.Color.blue())
            
            # Add thumbnail if examining an item or NPC
            if thumbnail_path:
                if thumbnail_path.startswith('http'):
                    embed.set_thumbnail(url=thumbnail_path)
                else:
                    # For local files, we need to handle them differently
                    # We'll send the image as an attachment and reference it
                    embed.set_thumbnail(url=f'attachment://{thumbnail_path.split("/")[-1]}')
            
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
            
            # Send with thumbnail file if needed
            if thumbnail_path and not thumbnail_path.startswith('http'):
                try:
                    file = discord.File(thumbnail_path)
                    await channel.send(file=file, embed=embed, view=view)
                except Exception as e:
                    print(f"Error sending thumbnail: {e}")
                    await channel.send(embed=embed, view=view)
            else:
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
#intents.message_content = True

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

TOKEN = config['DISCORD_TOKEN']
GUILD = config['DISCORD_SERVER']

client = DiscordBot(intents=intents, config=config)
client.run(TOKEN)

