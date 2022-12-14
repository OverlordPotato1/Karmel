import openai
import discord
import files
from variables import *
from discord import app_commands
import datetime
import asyncio

openai.api_key = files.loadJson("tokens.json")["openai"]

async def isBad(message):
    response = openai.Moderation.create(
        input = message.content
    )
    if not response.results[0].flagged:
        violations = "None"
        return False
    embed = discord.Embed(title="Content Policy Violation", description="The message you sent was determined to be in violation of OpenAI's content policy", color=0x3498db)
    embed.add_field(name="Message", value=message.content, inline=False)
    violations = []
    if response.results[0].categories["hate"]:
        violations += ["Hate Speech"]
    if response.results[0].categories["hate/threatening"]:
        violations += ["Threatening Speech"]
    if response.results[0].categories["self-harm"]:
        violations += ["Self Harm / Suicide"]
    if response.results[0].categories["sexual"]:
        violations += ["Sexual Content"]
    if response.results[0].categories["sexual/minors"]:
        violations += ["Sexual Content with Minors"]
    if response.results[0].categories["violence"]:
        violations += ["Violent Content"]
    if response.results[0].categories["violence/graphic"]:
        violations += ["Graphic Violence"]
    # combine the violations into a string and separate them with commas
    
    violations = ", ".join(violations)
    embed.add_field(name="Violations", value=violations, inline=False)
    await message.channel.send(embed=embed)
    print("Message sent by " + message.author.name + " failed moderation check. Violations: " + violations)
    return True

async def draw(message):
    if await isBad(message):
        return
    # check if message is a string
    if isinstance(message, str):
        prompt = message
    else:
        prompt = message.content
    async with message.channel.typing():
        
        try:
            response = openai.Image.create(
                prompt = prompt,
                n=1,
                size="512x512"
            )
        except openai.error.InvalidRequestError:
            embed = discord.Embed(title="Prompt rejected", description="openai.error.InvalidRequestError: Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by out safety system.")
            await message.channel.send(embed=embed)
            return response
        return response

async def gptWithoutMemory(message):
    if await isBad(message):
        return
    async with message.channel.typing():
            prompt = message.content.replace("Karmel, ", "")
            print('Sending prompt: "' + prompt + '" to OpenAI')
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                n=1,
                max_tokens=400
            )
    await message.channel.send(response.choices[0].text, reference=message)

async def gptWithMemory(message):
    if await isBad(message):
        return
    try:
        # do not run if the user has the "defining" trait in memory.json
        memory = files.loadJson("memory.json")
        if memory[str(message.author.id)]["defining"] == "true":
            return
        messageContent = message.content
        for i in range(0, len(activate)):
            if activate[i] in message.content:
                messageContent = message.content.replace(activate[i], "")
        # get the id of the bot
        messageContent = messageContent.replace("<@" + str(client.user.id) + ">", "")
        # read memory from file "memory.json"
        memory = files.loadJson("memory.json")
        try:
            test = memory[message.author.id]["message"]
        except:
            memory[str(message.author.id)]["message"] = "None"
            memory[str(message.author.id)]["response"] = "None"

        author = str(message.author.id)
        # if the user's name and gender are not in the dictionary memory, ask them
        async with message.channel.typing():
            # get the current time in UTC and convert it to a human readable format
            now = datetime.datetime.utcnow()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            now = str(now) + " UTC"
            # get the guild name
            try:
                guildName = message.guild.name
            except:
                guildName = "NOT IN SERVER"
            prompt = "{username:" + memory[author]["name"] + ", gender: " + memory[author]["gender"] + ", first seen: " + memory[author]["definitionDOW"] + " " + memory[author]["definitiondate"] + ' UTC}\nIt is currently '+ now + ', Server name: ' + guildName + '\n' + memory[author]["name"] + " (" + memory[author]["gender"] + "): " + memory[author]["message"] + "\n"+client.user.name+" (Female): " + memory[author]["response"] + "\n"+ memory[author]["name"] + " (" + memory[author]["gender"] + "): " + messageContent + "\n"+client.user.name+" (Female): "
            memory[author]["message"] = messageContent

            print(prompt)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                n=1,
                max_tokens=200
            )
            print(response.choices[0].text)
            memory[author]["response"] = response.choices[0].text
        # reply to the user with the response
        await message.channel.send(response.choices[0].text, reference=message)
        #save memory to file with json
        files.saveJson("memory.json", memory)
    except:
        await message.channel.send("An error occurred.  Please file a bug report at ")
        await gptWithoutMemory(message)
        raise


