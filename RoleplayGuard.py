import discord
from dotenv import get_key, load_dotenv
from ai import AI
from typing import *
from collections import defaultdict
import asyncio

from prompt import prompt

load_dotenv()

getenv = lambda key: get_key("Roleplay-Guard/env.env", key)

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
GROQ_API_KEY = getenv("GROQ_API_KEY")

ROLEPLAY_CHANNEL_ID = int(getenv("ROLEPLAY_CHANNEL_ID"))

ai = AI(GROQ_API_KEY)

intents = discord.Intents.all()
discord_client = discord.Client(intents=intents)

supervise = True

blocked_users = defaultdict(lambda: False) 
marked_users = defaultdict(lambda: 0)

async def clean_marks():
    await discord_client.wait_until_ready()
    channel = discord_client.get_channel(ROLEPLAY_CHANNEL_ID)

    while not discord_client.is_closed():
        await asyncio.sleep(3600)
        marked_users.clear()

        channel.send("Cleaned marks of all users!")

async def block_user(user: discord.User, channel: discord.TextChannel, allowed: bool):
    blocked_users[user.id] = not allowed
    overwrites = channel.overwrites_for(user)
    overwrites.send_messages = allowed
    await channel.set_permissions(user, overwrite=overwrites)
    

async def block_user_from_message(message: discord.Message, minutes: float):
    marked_users[message.author.id] =  0
    await block_user(message.author, message.channel, False)
    await message.channel.send(f"{message.author.name} has been blocked for {minutes} minutes.")
    await asyncio.sleep(60*minutes)
    await block_user(message.author, message.channel, True)
    await message.channel.send(f"{message.author.name} has been unblocked.")

def moderate_with_chat(message, context):
    return ai.chat(f"{prompt}\n\nContext:{context}\nMessage:{message}")



@discord_client.event
async def on_message(message: discord.Message):
    global supervise

    if message.author.bot:
        return
    
    if message.channel.id != ROLEPLAY_CHANNEL_ID:
        return

    if message.content in ["!toggle", "!supervise"]:
        supervise = not supervise
        await message.channel.send("✅ Started supervising" if supervise else "❌ Stopped supervising")
        return
    
    if not supervise:
        return
    
    context = []

    async for msg in message.channel.history(limit=5, before=message):
        context.append(msg.content)

    classification = moderate_with_chat(message=message.content, context=context)
    print(classification)

    if not "disapprove" in classification.lower():
        return
    
    marked_users[message.author.id] += 1

    if marked_users[message.author.id] == 3:
        await block_user_from_message(message, 2)

    else:
        await message.channel.send(f"{message.author.name} now has {marked_users[message.author.id]} {'mark' if marked_users[message.author.id] == 1 else 'marks'}.")

discord_client.run(DISCORD_TOKEN)