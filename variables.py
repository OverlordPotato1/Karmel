import discord
import openai
import files
from discord import app_commands
import datetime
import asyncio


activate = ["Karmel, ", "Karmel,", "karmel, ", "karmel,"]

TOKEN = files.loadJson("tokens.json")["discord"]

openai.api_key = files.loadJson("tokens.json")["openai"]

intents = discord.Intents(messages=True, guilds=True, members=True, presences=True, message_content = True)

client = discord.Client(intents=intents)

sharedMemory = files.dictionary


