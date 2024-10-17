This is a server that acts as a relay between a LlamaTale server and a Discord bot. It will send everyting coming from the server to Discord.
Steps:
1. Get and run LlamaTale
2. Configure LlamaTale-DiscordBot
   DISCORD_TOKEN:
   DISCORD_SERVER:
   llama_tale_path: # path to your LlamaTale folder
3. Run LlamaTale
4. Run LlamaTale-DiscordBot with `python discord_bot.py`
5. The bot will connect to your server.
6. In a private message, say `start` and it will connect to the LlamaTale server. There is sometimes a delay to the first message, unsure why.
7. Type commands like you would when normally playing LlamaTale.
8. Type `remind me` to make the bot resend the latest message. Useful if you reconnect, for example

It is currently not possible to restart the story.
It is only for 'if' mode.

Setting up a Discord bot:
   
You will need to set up a discord app/bot. Sadly, it's not possible for me to clone the existing one, it needs its own token etc.

You can do the first step in this tutorial for example: https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/

After that you need to add the bot to your discord server. The same tutorial has a step about this below the coding part.

LlamaTale-DiscordBot is free to use for personal purposes. Contact me if you wish to use it commercially.
