import discord
import files
import asyncio
import datetime
from variables import *
from OAI_Functions import isBad

async def defineMe(message):
    def check(m):
        return m.author.id == message.author.id
    # read memory from file "memory.json" using json
    memory = files.loadJson("memory.json")
    author = str(message.author.id)
    

    memory[author]["name"] = ""
    memory[author]["gender"] = ""
    memory[author]["definitiondate"] = ""
    memory[author]["definitionDOW"] = ""
    memory[author]["defining"] = "true"
    files.saveJson("memory.json", memory)


    embed = discord.Embed(title="What is your name?", description="", color=0x00ff00)
    # wait for a message from the user
    bad = True
    while bad :
        await message.channel.send(embed=embed)
        firstRun = False
        msg = await client.wait_for('message', check=check)
        bad = await isBad(msg)
    print(msg.author.id, msg.content)
    name = msg.content


    embed = discord.Embed(title="What is your gender?", description="", color=0x00ff00)
    
    bad = True
    while bad:
        await message.channel.send(embed=embed)
        firstRun = False
        msg = await client.wait_for('message', check=check)
        bad = await isBad(msg)


    async with message.channel.typing():
        await asyncio.sleep(1)
        memory = files.loadJson("memory.json")
    
        memory[author]["name"] = name
        memory[author]["gender"] = msg.content
        # get the current date and time in UTC
        memory[author]["definitiondate"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        memory[author]["definitionDOW"] = datetime.datetime.utcnow().strftime("%A")
        memory[author]["defining"] = "false"

        files.saveJson("memory.json", memory)