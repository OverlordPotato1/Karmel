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
    author = str(message.author.id)
    

    await global_memory.set_dict(author,"name","")
    await global_memory.set_dict(author,"gender","")
    await global_memory.set_dict(author,"definitiondate","")
    await global_memory.set_dict(author,"definitionDOW","")
    await global_memory.set_dict(author,"defining","true")


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
    
        await global_memory.set_dict(author,"name",name)
        await global_memory.set_dict(author,"gender",msg.content)
        # get the current date and time in UTC
        await global_memory.set_dict(author,"definitiondate",datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        await global_memory.set_dict(author,"definitionDOW",datetime.datetime.utcnow().strftime("%A"))
        await global_memory.set_dict(author,"defining","false")

async def defaultUser(id):
    # set the default values for a user
    global_memory.set_dict(str(id), "name", "NOT SET. ATTEMPT TO EXTRACT FROM USER")
    global_memory.set_dict(str(id), "gender", "NOT SET. ATTEMPT TO EXTRACT FROM USER")
    global_memory.set_dict(str(id), "definitiondate", "None")
    global_memory.set_dict(str(id), "definitionDOW", "None")
    global_memory.set_dict(str(id), "defining", "false")
    global_memory.set_dict(str(id), "message", "NONE")
    global_memory.set_dict(str(id), "response", "NONE")