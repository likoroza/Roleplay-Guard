from dis import disco
import discord
from dotenv import get_key, load_dotenv

load_dotenv()

getenv = lambda key: get_key("env.env", key)

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
ROLEPLAY_CHANNEL_ID = int(getenv("ROLEPLAY_CHANNEL_ID"))
ADMIN_ROLE_ID = int(getenv("ADMIN_ROLE_ID"))

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.channel.id != ROLEPLAY_CHANNEL_ID:
        return

client.run(DISCORD_TOKEN)