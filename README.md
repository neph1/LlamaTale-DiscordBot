This is a server that acts as a relay between a LlamaTale server and a Discord bot. It will send everyting coming from the server to Discord.
It provides some context related features.

<img width="703" height="633" alt="Screenshot from 2025-11-23 08-12-32" src="https://github.com/user-attachments/assets/cbeda794-d696-4ef3-9c27-2c7140b88c96" />


Steps:
1. Get and run LlamaTale
2. Configure LlamaTale-DiscordBot
   DISCORD_TOKEN:
   DISCORD_SERVER:
   llama_tale_path: # path to your LlamaTale folder
3. Run LlamaTale with the `--web` flag (it will open a browser which you can close
4. Run LlamaTale-DiscordBot with `python discord_bot.py`
5. The bot will connect to your server.
6. In a private message, say `start` and it will connect to the LlamaTale server. There is sometimes a delay to the first message, unsure why.
7. Type commands like you would when normally playing LlamaTale, OR use slash commands (see below).
8. Type `remind me` to make the bot resend the latest message. Useful if you reconnect, for example

## Slash Commands

<img width="661" height="516" alt="Screenshot from 2025-11-23 19-25-54" src="https://github.com/user-attachments/assets/09a9dfd7-3bef-46c3-bfa4-a66998e11c17" />


The bot supports slash commands for quick access to common game actions:

**Movement:**
- `/north`, `/south`, `/east`, `/west` - Move in cardinal directions

**Actions:**
- `/look` - Look around your current location
- `/take <item>` - Take an item
- `/drop <item>` - Drop an item
- `/examine <target>` - Examine something
- `/inventory` - Check your inventory

**Combat:**
- `/attack <target>` - Attack a target
- `/loot <target>` - Loot a target or container

**Equipment:**
- `/wear <item>` - Wear an item
- `/wield <weapon>` - Wield a weapon

**Interaction:**
- `/say <message>` - Say something
- `/give <item> <target>` - Give an item to someone
- `/use <item> [target]` - Use an item
- `/open <target>` - Open a door or container
- `/close <target>` - Close a door or container
- `/help` - Show available commands

You can also type commands directly in the chat (e.g., "look", "north", etc.)

It is currently not possible to restart the story.
It is only for 'if' mode. But I think adding MUD support won't be very difficult.

Setting up a Discord bot:
   
You will need to set up a discord app/bot. Sadly, it's not possible for me to clone the existing one, it needs its own token etc.

You can do the first step in this tutorial for example: https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/

After that you need to add the bot to your discord server. The same tutorial has a step about this below the coding part.

It might be obvious, but from a privacy stand point, this is not an optimal solution, since all data passes through Discords servers.

LlamaTale-DiscordBot is free to use for personal purposes. Contact me if you wish to use it commercially.

