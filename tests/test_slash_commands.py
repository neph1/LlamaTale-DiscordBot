"""Tests for Discord slash commands."""
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord import app_commands


class TestSlashCommands:
    """Test slash command functionality."""
    
    @patch('discord_bot.LlamaTaleInterface')
    def test_setup_commands_creates_command_tree(self, mock_llama):
        """Test that command tree is created with slash commands."""
        from discord_bot import DiscordBot
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        config = {
            'DISCORD_TOKEN': 'test_token',
            'DISCORD_SERVER': 'test_server',
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale'
        }
        
        bot = DiscordBot(intents=intents, config=config)
        
        # Verify command tree is created
        assert bot.tree is not None
        assert isinstance(bot.tree, app_commands.CommandTree)
    
    @patch('discord_bot.LlamaTaleInterface')
    def test_all_required_commands_registered(self, mock_llama):
        """Test that all required slash commands are registered."""
        from discord_bot import DiscordBot
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        config = {
            'DISCORD_TOKEN': 'test_token',
            'DISCORD_SERVER': 'test_server',
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale'
        }
        
        bot = DiscordBot(intents=intents, config=config)
        
        # Get all registered command names
        command_names = [cmd.name for cmd in bot.tree.get_commands()]
        
        # Required commands from the issue
        required_commands = [
            'look', 'say', 'take', 'attack', 'north', 'south', 'east', 'west',
            'loot', 'wear', 'wield', 'drop', 'examine', 'open', 'close', 
            'use', 'inventory', 'help', 'give'
        ]
        
        # Check all required commands are registered
        for cmd in required_commands:
            assert cmd in command_names, f"Command '{cmd}' is not registered"
        
        # Verify we have exactly the expected number of commands
        assert len(command_names) == len(required_commands), \
            f"Expected {len(required_commands)} commands, got {len(command_names)}"
    
    @patch('discord_bot.LlamaTaleInterface')
    async def test_command_requires_channel(self, mock_llama):
        """Test that commands check if channel is set."""
        from discord_bot import DiscordBot
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        config = {
            'DISCORD_TOKEN': 'test_token',
            'DISCORD_SERVER': 'test_server',
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale'
        }
        
        bot = DiscordBot(intents=intents, config=config)
        
        # Mock interaction
        interaction = MagicMock(spec=discord.Interaction)
        interaction.response = MagicMock()
        interaction.response.send_message = AsyncMock()
        
        # Channel is not set (None)
        bot.channel = None
        
        # Get the look command
        look_cmd = None
        for cmd in bot.tree.get_commands():
            if cmd.name == 'look':
                look_cmd = cmd
                break
        
        assert look_cmd is not None, "Look command not found"
        
        # Execute the command
        await look_cmd.callback(interaction)
        
        # Verify it sent an error message
        interaction.response.send_message.assert_called_once()
        call_args = interaction.response.send_message.call_args
        assert "start the game first" in call_args[0][0].lower()
    
    @patch('discord_bot.LlamaTaleInterface')
    async def test_check_channel_method(self, mock_llama):
        """Test the _check_channel helper method."""
        from discord_bot import DiscordBot
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        config = {
            'DISCORD_TOKEN': 'test_token',
            'DISCORD_SERVER': 'test_server',
            'url': 'http://localhost',
            'port': 8180,
            'endpoint': '/tale'
        }
        
        bot = DiscordBot(intents=intents, config=config)
        
        # Mock interaction
        interaction = MagicMock(spec=discord.Interaction)
        interaction.response = MagicMock()
        interaction.response.send_message = AsyncMock()
        
        # Test with no channel
        bot.channel = None
        result = await bot._check_channel(interaction)
        assert result is False
        interaction.response.send_message.assert_called_once()
        
        # Test with channel set
        interaction.response.send_message.reset_mock()
        bot.channel = MagicMock()
        result = await bot._check_channel(interaction)
        assert result is True
        interaction.response.send_message.assert_not_called()

