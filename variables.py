import discord
import openai
import files
from discord import app_commands
import datetime
import asyncio
import os

useBeta = True

activate = ["Karmel, ", "Karmel,", "karmel, ", "karmel,"]

TOKEN = files.loadJson("tokens.json")["discord"]
# if useBeta:
#     discordToken = os.environ.get("KARMEL_PRE_API")
# else:
#     discordToken = os.environ.get("KARMEL_MAIN_API")

openai.api_key = os.environ.get("OPENAI_API")

intents = discord.Intents(messages=True, guilds=True, members=True, presences=True, message_content = True)

client = discord.Client(intents=intents)

sharedMemory = files.dictionary


