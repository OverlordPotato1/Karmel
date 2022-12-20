import files
import discord
from variables import *
import datetime
import asyncio
from user_management import *
from OAI_Functions import *
import wit_Handling


async def activated(message, isPing=False):

    timeUTC = datetime.datetime.utcnow()
    timeDay = timeUTC.strftime("%Y-%m-%d")
    timeSubDay = timeUTC.strftime("%H:%M:%S")
    authorId = str(message.author.id)

    if not await global_memory.checkExists_category(authorId):
        await global_memory.set_dict(authorId, "name", "")
        await global_memory.set_dict(authorId, "gender", "")
        await global_memory.set_dict(authorId, "defining", "false")
        await global_memory.set_dict(authorId, "imageCount", 0)
        await global_memory.set_dict(authorId, "allowImage", "true")
        await global_memory.set_dict(authorId, "imageLastUsed", "0")
        await global_memory.set_dict(authorId, "dmDisclaimer", "false")

    def sameAuthor(m):
        return m.author.id == message.author.id
    # make sure the user is not a bot
    #check if the messaged pinged karmel

    if message.author.bot:
        return

    # if isPing and "<@" not in message.content:
    #     isPing = False

    # ensure its not a @everyone or @here ping
    if isPing == True and "<@"+str(client.user.id)+">" not in message.content:
        print("ignoring @everyone ping")
        return
    newMessage = message.content.replace("Karmel, ", "")
    # remove karmel's ping
    newMessage = newMessage.replace("<@"+str(client.user.id)+">", "")
    newMessage = newMessage.lower()

    # response = await wit_Handling.CAR(message)

    # if newMessage == "define me":

    #     await defineMe(message)
    #     # tell the user that they have been defined
    #     await message.channel.send("You are now in memory")
    #     return

    #################################################
    # POTENTIAL SOURCE OF CRASH. MAY NEED REWORKING #
    #################################################

    # if str(message.author.id) not in memory and newMessage != "forget me":
    #     await defineMe(message)

    #################################################
    # / / / / / / / / / / / / / / / / / / / / / / / #
    #################################################

    # if newMessage == "who am i":
    #     # read memory from file "memory.json" using json
    #     memory = files.loadJson("memory.json")
    #     author = str(message.author.id)
    #     # if the user is in the dictionary memory, tell them their name
    #     if author in memory:
    #         await message.channel.send("{'<@" + str(author) + ">': " + str(memory[author]) + "}")
    #     else:
    #         await message.channel.send("I don't know, do you wish to be defined?")
    #         # wait for a response
    #         response = await client.wait_for("message", check=sameAuthor)
    #         # if the response is yes, define them
    #         if response.content.lower() == "yes":
    #             await defineMe(message)
    #     return

    if newMessage == "sync":
        # ensure the user has the id 441688723344719882
        if message.author.id == 441688723344719882:
            # read memory from file "memory.json" using json
            memory = files.loadJson("memory.json")
            # read servers from file "servers.json" using json
            servers = files.loadJson("servers.json")
            # for each server in servers
            for server in servers:
                # get the server object
                serverObj = client.get_guild(int(server))
                # for each member in the server
                for member in serverObj.members:
                    # if the member is not in memory, add them
                    if str(member.id) not in memory:
                        memory[str(member.id)] = member.name
            # save memory to file with json
            files.saveJson("memory.json", memory)
            await message.channel.send("Synced commands with servers")
        else:
            await message.channel.send("You do not have permission to do that")
        global_memory.reload()
        return

    if newMessage == "forget our conversation":
        await global_memory.set_dict(str(message.author.id), "message", "")
        await global_memory.set_dict(str(message.author.id), "response", "")
        embed = discord.Embed(title="Conversation Deleted", description="", color=0x00ffff)
        message.response(embed=embed)
        return

    if newMessage == "alter memory":
        # ensure the user has the
        if message.author.id == 441688723344719882:
            # read memory from file "memory.json" using json
            memory = files.loadJson("memory.json")
            memory[str(message.author.id)]["defining"] = "true"
            files.saveJson("memory.json", memory)
            # ask the user what they want to do
            await message.channel.send("What would you like to do? (read, write, delete)")
            # wait for a response
            response = await client.wait_for("message", check=sameAuthor)
            # if the response is read
            if response.content.lower() == "read":
                # ask the user what they want to read
                await message.channel.send("What would you like to read? (user, server)")
                # wait for a response
                response = await client.wait_for("message", check=sameAuthor)
                # if the response is user
                if response.content.lower() == "user":
                    # ask the user what user they want to read
                    await message.channel.send("What user would you like to read? (mention)")
                    # wait for a response
                    response = await client.wait_for("message", check=sameAuthor)
                    # if the response is a mention
                    if response.mentions:
                        # read the user's memory
                        await message.channel.send(memory[str(response.mentions[0].id)])
                    else:
                        await message.channel.send("That is not a user")
                # if the response is server
                elif response.content.lower() == "server":
                    # read the server's memory
                    await message.channel.send(memory[str(message.guild.id)])
                else:
                    await message.channel.send("That is not a valid option")
            # if the response is write
            elif response.content.lower() == "write":
                # ask the user what they want to write
                await message.channel.send("What would you like to write? (user, server)")
                # wait for a response
                response = await client.wait_for("message", check=sameAuthor)
                # if the response is user
                if response.content.lower() == "user":
                    # ask the user what user they want to write
                    await message.channel.send("What user would you like to write? (mention)")
                    # wait for a response
                    response = await client.wait_for("message", check=sameAuthor)
                    # if the response is a mention
                    if response.mentions:
                        # ask the user what they want to write
                        await message.channel.send("What variable would you like to edit? (case sensitive)")
                        # wait for a response
                        response2 = await client.wait_for("message", check=sameAuthor)
                        # ask the user what they want to write
                        await message.channel.send("str or int?")
                        # wait for a response
                        response3 = await client.wait_for("message", check=sameAuthor)
                        # if the response is str
                        if response3.content.lower() == "str":
                            # ask the user what they want to write
                            await message.channel.send("What would you like to write?")
                            # wait for a response
                            response4 = await client.wait_for("message", check=sameAuthor)
                            # write the user's memory
                            memory = files.loadJson("memory.json")
                            memory[str(response.mentions[0].id)][response2.content] = response4.content
                            files.saveJson("memory.json", memory)
                        # if the response is int
                        elif response3.content.lower() == "int":
                            # ask the user what they want to write
                            await message.channel.send("What would you like to write?")
                            # wait for a response
                            response4 = await client.wait_for("message", check=sameAuthor)
                            # write the user's memory
                            memory = files.loadJson("memory.json")
                            memory[str(response.mentions[0].id)][response2.content] = int(response4.content)
                            files.saveJson("memory.json", memory)
                # if the response is server
                elif response.content.lower() == "server":
                    # ask the user what they want to write
                    await message.channel.send("What would you like to write?")
                    # wait for a response
                    response = await client.wait_for("message", check=sameAuthor)
                    # write the server's memory
                    memory[str(message.guild.id)] = response.content
                    await message.channel.send("Written")
                else:
                    await message.channel.send("That is not a valid option")
            # if the response is delete
            elif response.content.lower() == "delete":
                # ask the user what they want to delete
                await message.channel.send("What would you like to delete? (user, server)")
                # wait for a response
                response = await client.wait_for("message", check=sameAuthor)
                # if the response is user
                if response.content.lower() == "user":
                    # ask the user what user they want to delete
                    await message.channel.send("What user would you like to delete? (mention)")
                    # wait for a response
                    response = await client.wait_for("message", check=sameAuthor)
                    # if the response is a mention
                    if response.mentions:
                        # delete the user's memory
                        del memory[str(response.mentions[0].id)]
                        await message.channel.send("Deleted")
                    else:
                        await message.channel.send("That is not a user")
                # if the response is server
                elif response.content.lower() == "server":
                    # delete the server's memory
                    del memory[str(message.guild.id)]
                    await message.channel.send("Deleted")
                else:
                    await message.channel.send("That is not a valid option")
            embed = discord.Embed(title="Memory", description="Memory editor exited", color=0x00ff00)
            await message.channel.send(embed=embed)
            await asyncio.sleep(1)
            memory[str(message.author.id)]["defining"] = "false"
            files.saveJson("memory.json", memory)
            # fuck this shit i didn't even write this there no way in hell i'm fixing it to use the new memory system
            global_memory.reload()
        return

    if newMessage == "draw a picture":

        async with message.channel.typing():
            skipCheck = False
            # give the user the defining status
            await global_memory.set_dict(authorId, "defining", "true")


            if not global_memory.checkExists_variable(authorId, "allowImage"):
                await global_memory.set_dict(authorId, "allowImage", "true")
                await global_memory.set_dict(authorId, "imageCount", 0)
                await global_memory.set_dict(authorId, "imageLastUsed", "NEVER")


            if await global_memory.read_dict(authorId, "imageLastUsed") != timeDay:
                await global_memory.set_dict(authorId, "imageCount", 0)
                await global_memory.set_dict(authorId, "allowImage", "true")
                await global_memory.set_dict(authorId, "imageLastUsed", timeDay)
                skipCheck = True


            if await global_memory.read_dict(authorId, "allowImage") == "false" and skipCheck == False:
                embed = discord.Embed(title="Image Limit Reached", description="You have reached the image limit today", color=0xff0000)
                embed.set_footer(text="You can use images again tomorrow")
                await message.channel.send(embed=embed)
                return
            
            
            if await global_memory.read_dict(authorId, "imageCount") >= 25 and skipCheck == False:
                await global_memory.set_dict(authorId, "allowImage", "false")
                embed = discord.Embed(title="Image Limit Reached", description="You have reached the image limit today", color=0xff0000)
                embed.set_footer(text="You can use images again tomorrow")
                await message.channel.send(embed=embed)
                return
        
        
        

        bad = True
        while bad:
            embed = discord.Embed(title="What would you like to draw?", description="Keep it SFW", color=0x00ff00)
            msg = await message.channel.send(embed=embed)
            response = await client.wait_for("message", check=sameAuthor)
            bad = await isBad(response)
            if bad:
                rejected = discord.Embed(title="Rejected", description="Your prompt returned rejected", color=0xff0000)
        await msg.delete()

        async with message.channel.typing():
            embed = discord.Embed(title="Please Wait", description="Submitting prompt to OpenAI", color=0x00ff00)
            embed.set_footer(text="This should only take a few seconds")
            msg = await message.channel.send(embed=embed)
            image = await draw(response)
            await msg.delete()
            # send the response and reply to the original message
            embed = discord.Embed(title="Image Complete", description="", color=0x00ff00)
            # the image is a url in the variable image
            await message.channel.send(image['data'][0]['url'])
            global_memory.add_dict(authorId, "imageCount", 1)
            global_memory.set_dict(authorId, "defining" , "false")
            global_memory.set_dict(authorId, "imageLastUsed", timeDay)
            memoryHandler(authorId, 'COMMAND.DRAW_PICTURE "', 'PROMPT: "'+response+'"')
            skipCheck = False
        return

    if newMessage.split(" ")[0] == "with" and newMessage.split(" ")[1] == "codex":
        # remove "with codex" from the message
        message.content = newMessage.replace("with codex ", "")
        # send the message to use_codex
        async with message.channel.typing():
            await use_codex(message)
        return

    await global_memory.save()

    await gptWithMemory(message)