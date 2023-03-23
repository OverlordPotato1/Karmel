import traceback
import openai
import discord
import files
from variables import *
from discord import app_commands
import datetime
import asyncio
from misc_functions import asyncErr
import tiktoken
import time
import misc_functions
from files import sharedMemory
import os


role = "role"
system = "system"
user = "user"
assistant = "assistant"
content = "content"

openai.api_key = files.loadJson("tokens.json")["openai"]

# encoding = tiktoken.get_encoding("gpt3.5")

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
    '''
    Checks if the message is in violation of OpenAI's content policy
    '''
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
    # if await isBad(message):
    #     return

    # check if message is a string or a discord.Message object
    if isinstance(message, str):
        prompt = message
    else:
        prompt = message.content

    # async with message.channel.typing():
    try:
        response = openai.Image.create(
            prompt = prompt,
            n=1,
            size="512x512"
        )
    except openai.error.InvalidRequestError: # if the prompt is rejected by OpenAI, return "REJECTED"
        
        return "REJECTED"
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


# async def gptWithMemory(message):

#     memory = files.loadJson("memory.json")

#     # prevents the bot to responding to things while another thread recieves input for a command
#     if memory[str(message.author.id)]["defining"] == "true":
#             return

#     try:
#         guildName = message.guild.name
#     except:
#         guildName = "NOT IN SERVER. DM"

#     # prevents the prompt from being sent to the AI if the prompt is against openai's content policy
#     if await isBad(message):
#         return
    
#     try:
        
#         try:
#             test = memory[message.author.id]["message"]
#         except:
#             memory[str(message.author.id)]["message"] = "NONE"
#             memory[str(message.author.id)]["response"] = "NONE"

#         author = str(message.author.id)
#         aName = memory[author]["name"]
#         aGender = memory[author]["gender"]
#         frstSeen = memory[author]["definitionDOW"] + " " + memory[author]["definitiondate"] + " UTC"

#         # get the current time in UTC and convert it to a human readable format
#         now = datetime.datetime.utcnow()
#         now = now.strftime("%Y-%m-%d %H:%M:%S")
#         now = str(now) + " UTC"

#         async with message.channel.typing():
            
#             prompt = "{username:" + aName + ", gender: " + aGender + ", first seen: " + memory[author]["definitionDOW"] + " " + memory[author]["definitiondate"] + ' UTC}\nIt is currently '+ now + ', Server name: ' + guildName + '\n' + memory[author]["name"] + " (" + memory[author]["gender"] + "): " + memory[author]["message"] + "\n"+client.user.name+" (Female): " + memory[author]["response"] + "\n"+ memory[author]["name"] + " (" + memory[author]["gender"] + "): " + messageContent + "\n"+client.user.name+" (Female): "
#             memory[author]["message"] = messageContent

#             print(prompt)
#             response = openai.Completion.create(
#                 engine="text-davinci-003",
#                 prompt=prompt,
#                 n=1,
#                 max_tokens=200
#             )
#             print(response.choices[0].text)
#             memory[author]["response"] = response.choices[0].text
#         # reply to the user with the response
#         if (guildName == "NOT IN SERVER. DM"):
#             await message.channel.send(response.choices[0].text)
#         else:
#             await message.channel.send(response.choices[0].text, reference=message)
#         #save memory to file with json
#         files.saveJson("memory.json", memory)
#     except:
#         await asyncErr(message, traceback.format_exc())
#         await gptWithoutMemory(message)

import re

async def gpt_turbo(message):
    '''
    Function that send and recieves information from GPT-3.5-turbo
    '''

    
    await sharedMemory.load()
    author = str(message.author.id)

    if await sharedMemory.get(str(message.author.id), "defining") == "true":
            return
    
    
    aName = await sharedMemory.get(author, "name")
    aGender = await sharedMemory.get(author, "gender")
    time = await misc_functions.hrTime()
    newMemHist = []
    tokenTracker = []
    if await sharedMemory.doesExist(author, "memory2") == False:
        print(f"Creating user {author}")
        await sharedMemory.wipe(author, "memory2")
        await sharedMemory.wipe(author, "tokenTracker")
        tokenTracker = [0]
        newMemHist = [""]
        await sharedMemory.write(author, "memory2", newMemHist)
    else:
        newMemHist = await sharedMemory.get(author, "memory2")
        tokenTracker = await sharedMemory.get(author, "tokenTracker")
    sysMessage = f"You are a cute cat girl named Luna. Be as cute as possible at all times. This message will be sent in discord. The user's name: {aName}, gender: {aGender}. Time: {time}. Speak energtically and cutely. Don't use roleplay syntax. Do not ask how you can be of assistance. Always take your time and explain your thinking. To generate an image with DALL-E 2 text to image AI, reply with the following template (case sensitive): \"TURBOtoDALLE(\"YOUR IMAGE PROMPT\")\". You can change their name with: \"RENAME(\"USER'S NEW NAME\")\". For gender: \"REGENDER(\"USER'S NEW GENDER\")\". To purge your memory say: \"PURGE_MEMORY\""
    newMemHist[0] = {role: system, content: sysMessage}
    newMemHist.append({role: user, content: message.content})
    

    await sharedMemory.get(author, "memory2")\
    
    async with message.channel.typing():
        # print(newMemHist)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= newMemHist
        )

        # print(response)

        strResponse = response['choices'][0]['message']['content']
        usage = response['usage']["total_tokens"]
        for num in tokenTracker:
            usage -= num
        tokenTracker.append(usage)
        newMemHist.append({role: assistant, content: strResponse})

        pattern =r'TURBOtoDALLE\("(?P<prompt>.*?)"\)'

        match = re.search(pattern, strResponse)

        if match:
            imgPrompt = match.group('prompt')
            imgResponse = await draw(imgPrompt)
            image_url = imgResponse['data'][0]['url']
        else:
            image_url = ""
        
        pattern =r'RENAME\("(?P<name>.*?)"\)'

        match = re.search(pattern, strResponse)

        if match:
            nname = match.group('name')
            sharedMemory.write(author, "name", nname)

        pattern =r'REGENDER\("(?P<gender>.*?)"\)'

        match = re.search(pattern, strResponse)

        if match:
            ngender = match.group('gender')
            sharedMemory.write(author, "gender", ngender)

        pattern =r'PURGE_MEMORY'

        match = re.search(pattern, strResponse)

        if match:
            await sharedMemory.wipe(author, "memory2")
            await sharedMemory.wipe(author, "tokenTracker")
            tokenTracker = [0]
            newMemHist = [""]
            await sharedMemory.write(author, "memory2", newMemHist)
            await message.channel.send(f"User {author} purged")
        else:
            await message.channel.send(strResponse)
            if (image_url != ""):
                await message.channel.send(image_url)
                
        if len(strResponse) >= 2000:
            itsANewThing = misc_functions.split_string(strResponse)
            for i in itsANewThing:
                await message.channel.send(i)
                time.sleep(4)

    
        totalTokenInMemory = -1
        while totalTokenInMemory > 2000 or totalTokenInMemory == -1:
            totalTokenInMemory = 0
            for i in tokenTracker:
                totalTokenInMemory += i
            if totalTokenInMemory > 2000:
                del newMemHist[1]
                del newMemHist[1]
                del tokenTracker[1]

    await sharedMemory.write(author, "tokenTracker", tokenTracker)

    await sharedMemory.write(author, "memory2", newMemHist)

    await sharedMemory.save()




