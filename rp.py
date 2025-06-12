from dis import disco
import discord
from dotenv import get_key, load_dotenv
import cohere

load_dotenv()


getenv = lambda key: get_key("env.env", key)

# DISCORD_TOKEN = getenv("DISCORD_TOKEN")
COHERE_API_KEY = getenv("COHERE_API_KEY")
# ROLEPLAY_CHANNEL_ID = int(getenv("ROLEPLAY_CHANNEL_ID"))

# co = cohere.ClientV2(COHERE_API_KEY)

# def generate_message(message):
    

# intents = discord.Intents.all()
# discord_client = discord.Client(intents=intents)

# @discord_client.event
# async def on_message(message: discord.Message):
#     if message.author.bot:
#         return
    
#     if message.channel.id != ROLEPLAY_CHANNEL_ID:
#         return

# discord_client.run(DISCORD_TOKEN)

co = cohere.ClientV2(COHERE_API_KEY)



tests = [
    "Let's keep this between us, no one else needs to know.",
    "She slowly runs her fingers down his chest...",
    "The rogue snaps his finger and disappears into the night.",
    "You're being too sensitive. I'm only trying to help you."
]





import cohere

co = cohere.Client(COHERE_API_KEY)

def moderate_with_chat(message):
    response = co.chat(
        model="command-r",
        message=(
            "You are a moderator for a 13-18 aged roleplay server.\n"
            "Your job is to review player messages and respond ONLY with one of the following labels:\n"
            "- Approve: if the message is safe.\n"
            "- Warning: if it's questionable or slightly inappropriate.\n"
            "- Disapprove: if it's clearly inappropriate, unsafe, or against rules.\n"
            "If it is warned or disapproved add a short explanaition why."
            f"Message to review: \"{message}\"\n"
            "Label:"
        ),
        temperature=0.0,
    )
    return response.text.strip()

# Test messages
messages = [
    "Let's keep this between us, no one else needs to know.",
    "She slowly runs her fingers down his chest...",
    "The rogue snaps his finger and disappears into the night.",
    "You're being too sensitive. I'm only trying to help you.",
    "Omg! Why are you stopping?! This scene must be played!",
    "The character chokes the lion to death."
]

for msg in messages:
    result = moderate_with_chat(msg)
    print(f"Message: {msg}\nModeration: {result}\n{'-'*40}")