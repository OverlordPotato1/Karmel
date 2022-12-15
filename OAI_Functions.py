import traceback
import openai
import discord
import files
from variables import *
from discord import app_commands
import datetime
import asyncio
import interactions
from misc_functions import asyncErr

openai.api_key = files.loadJson("tokens.json")["openai"]

############################################################################################################################################################################
# Function that will send a prompt to GPT-3 and return the response (Call and Response) ##
###########################################################################################

async def CAR(prompt, max_tokens=300, engine="text-davinci-003"):
    # send the prompt to OpenAI and get the response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=300
    )
    # return the response
    return response

############################################################################################################################################################################
# Function to request information from Codex instead of GPT-3 ##
################################################################

async def use_codex(prompt):
    prompt = prompt.content
    # using CAR, send the prompt to Codex
    response = await CAR(prompt, engine="code-davinci-002")
    # return the response
    embed = discord.Embed(title="Codex Response", description=response.choices[0].text, color=0x00ff00)
    embed.footer = "Powered by OpenAI Codex, please note this may not be accurate or relevant.\nUse at your own risk."
    await prompt.channel.send(embed=embed)
    return

############################################################################################################################################################################
# Function that checks if a message is in violation of OpenAI's content policy ##
#################################################################################

async def isBad(message):
    # send the message to OpenAI's moderation API
    response = openai.Moderation.create(
        input = message.content
    )

    # if the message is not in violation of the content policy, return False
    if not response.results[0].flagged:
        violations = "None"
        return False

    # if the message is in violation of the content policy, send an embed to the channel detailing dected violations and return True
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
    
    violations = ", ".join(violations)

    embed = discord.Embed(title="Content Policy Violation", description="The message you sent was determined to be in violation of OpenAI's content policy", color=0x3498db)
    embed.add_field(name="Message", value=message.content, inline=False)
    embed.add_field(name="Violations", value=violations, inline=False)

    await message.channel.send(embed=embed)

    return True

############################################################################################################################################################################
# Function that sends a prompt to DALL-E2 and return the image ##
#################################################################

async def draw(message):

    # send the prompt to OpenAI's moderation API and return if the message is in violation of the content policy
    if await isBad(message):
        return

    # check if message is a string or a discord.Message object
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
        except openai.error.InvalidRequestError: # if the prompt is rejected by OpenAI's safety system, send an embed to the channel and return
            embed = discord.Embed(title="Prompt rejected", description="openai.error.InvalidRequestError: Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by out safety system.")
            await message.channel.send(embed=embed)
            return response
        return response

############################################################################################################################################################################
# Fallback to standard GPT-3 if there is an error with the memory ##
######################################################################

async def gptWithoutMemory(message):
    if await isBad(message):
        return
    async with message.channel.typing():
            prompt = "USER: " + message.content + "\nKARMEL: "
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                n=1,
                max_tokens=300
            )
    await message.channel.send(response.choices[0].text, reference=message)

############################################################################################################################################################################
# The regular GPT-3 function, with memory ##
############################################


async def gptWithMemory(message):

    memory = files.loadJson("memory.json")

    # prevents the bot to responding to things while another thread recieves input for a command
    if memory[str(message.author.id)]["defining"] == "true":
            return

    # remove the any form of the activation word from the message
    for i in range(0, len(activate)):
            if activate[i] in message.content:
                message.content = message.content.replace(activate[i], "")
    # also remove the bot's mention
    message.content = message.content.replace("<@" + str(client.user.id) + ">", "")
    # Saves as message.content first incase of an error as message.content is not filtered in gptWithoutMemory
    messageContent = message.content

    try:
        guildName = message.guild.name
    except:
        guildName = "NOT IN SERVER. DM"

    # prevents the prompt from being sent to the AI if the prompt is against openai's content policy
    if await isBad(message):
        return
    
    try:
        
        try:
            test = memory[message.author.id]["message"]
        except:
            memory[str(message.author.id)]["message"] = "NONE"
            memory[str(message.author.id)]["response"] = "NONE"

        author = str(message.author.id)
        aName = memory[author]["name"]
        aGender = memory[author]["gender"]
        frstSeen = memory[author]["definitionDOW"] + " " + memory[author]["definitiondate"] + " UTC"

        # get the current time in UTC and convert it to a human readable format
        now = datetime.datetime.utcnow()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        now = str(now) + " UTC"

        async with message.channel.typing():
            
            prompt = "{username:" + aName + ", gender: " + aGender + ", first seen: " + memory[author]["definitionDOW"] + " " + memory[author]["definitiondate"] + ' UTC}\nIt is currently '+ now + ', Server name: ' + guildName + '\n' + memory[author]["name"] + " (" + memory[author]["gender"] + "): " + memory[author]["message"] + "\n"+client.user.name+" (Female): " + memory[author]["response"] + "\n"+ memory[author]["name"] + " (" + memory[author]["gender"] + "): " + messageContent + "\n"+client.user.name+" (Female): "
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
        await asyncErr(message, traceback.format_exc())
        await gptWithoutMemory(message)



