import discord
import openai
import files
from discord import app_commands
import datetime
import asyncio
import interactions

activate = ["Karmel, ", "Karmel,", "karmel, ", "karmel,"]

TOKEN = files.loadJson("tokens.json")["discord"]

openai.api_key = files.loadJson("tokens.json")["openai"]

intents = discord.Intents(messages=True, guilds=True, members=True, presences=True, message_content = True)

client = discord.Client(intents=intents)

global_memory = files.async_dictionary("memory.json")




