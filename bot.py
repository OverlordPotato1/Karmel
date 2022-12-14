import datetime
import os
import openai
import youtube_dl
import asyncio
import files
from OAI_Functions import *
from variables import *
from primary_activated import *
import discord

bot = app_commands.CommandTree(client)

memory = {}

#########################################
#                                       #
#   Definitions                         #
#                                       #
#########################################



def determineSource(message):
    if "https://www.youtube.com/watch?v=" in message:
        return "youtube"
    elif "https://open.spotify.com/track/" in message:
        #if its a spotify link
        return "spotify"
    else:
        return message
        
#########################################
#                                       #
#   Bot Commands                        #
#                                       #
#########################################

@bot.command(name = "settings", description="Change the settings for the bot")
async def settings(interaction):
    embed = discord.Embed(title="Settings", description="Change the settings for the bot", color=0x00ff00)
    embed.add_field(name="Welcome Channel", value="Change the welcome channel the bot will use", inline=False)
    embed.add_field(name="Command Prefix", value="Change the prefix the bot will use for commands", inline=False)
    embed.add_field(name="Variables", value="Modify the bot's server variables", inline=False)
    embed.add_field(name="Greeting Style", value="Modify the way GPT-3 will greet a user on join", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 441688723344719882:
        await bot.sync()
        print('Command tree synced.')
        embed = discord.Embed(title="Synced", description="Command tree synced", color=0x00ff00)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title="Invalid User ID", description="This command can only be used by the bot creator", color=0xe74c3c)
        await interaction.response.send_message(embed=embed)

@bot.command(name='ban', description='Ban a user from the server')
async def ban(interaction: discord.Interaction, user: discord.User, *, generate_reason: bool=False, delete_message_days: int = 0, reason: str = None):
    # if the ban command is not used in a guild
    if not interaction.guild:
        # make embed
        embed = discord.Embed(title="Invalid usage", description="This command can only be used in a server", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # make sure parameters have been provided
    if not user:
        # make embed
        embed = discord.Embed(title="Invalid usage", description="You must provide a user to ban", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # make sure the delete_message_days parameter is valid
    if delete_message_days < 0 or delete_message_days > 7:
        # make embed
        embed = discord.Embed(title="Invalid usage", description="The delete_message_days parameter must be between 0 and 7", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # ensure the user has the correct permissions
    if not interaction.user.guild_permissions.ban_members:
        # make embed
        embed = discord.Embed(title="Insufficient permissions", description="You do not have permission to use this command", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # ensure the bot has the correct permissions
    if not interaction.guild.me.guild_permissions.ban_members:
        # make embed
        embed = discord.Embed(title="Permission Error", description="I do not have permission to ban users", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the user is not in the server
    if user not in interaction.guild.members:
        # make embed
        embed = discord.Embed(title="Unknown user", description="That user is not in the server", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the user is the bot
    if user == interaction.guild.me:
        # make embed
        embed = discord.Embed(title="Self Protection", description="I cannot ban myself", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the user is the owner
    if user == interaction.guild.owner:
        # make embed
        embed = discord.Embed(title="Invalid Target", description="I cannot ban the owner", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the user is the author
    if user == interaction.user:
        # make embed
        embed = discord.Embed(title="Invalid Target", description="I cannot the executer", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the user has higher permissions than the author
    if user.top_role.position > interaction.user.top_role.position:
        # make embed
        embed = discord.Embed(title="Insufficient Superiority", description="That user is a higher rank than you", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return

    # if the target has higher permissions than the user
    if user.top_role.position > interaction.guild.me.top_role.position:
        # if the user is the owner
        if user == interaction.guild.owner:
            pass
        else:
            # make embed
            embed = discord.Embed(title="Insufficient Superiority", description="That user is a higher rank than me", color=0xe74c3c)
            # send embed
            await interaction.response.send_message(embed=embed)
            return
    # send the user the reason
    if generate_reason:
        # get the reason
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="The user's name is: " + user.name + "\nThe server's name is: " + interaction.guild.name + "The admin who banned them provided this reason as a prompt: " + reason + "\nKarmel: ",
            n=1,
            max_tokens=200
        )
        # set the reason
        reason = response["choices"][0]["text"]
    # pm the user the reason
    await user.send("You have been banned from " + interaction.guild.name + " for the following reason: " + reason)
    # ban the user
    await interaction.guild.ban(user, delete_message_days=delete_message_days, reason=reason)
            
    await interaction.response.send_message(f'{user} was banned from the server.')

@bot.command(name="uban", description="Unbans a user from the server")
async def uban(interaction: discord.Interaction, user: discord.User):
    # if not used in a guild
    if not interaction.guild:
        # make embed
        embed = discord.Embed(title="Invalid usage", description="This command can only be used in a server", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # ensure the user has the correct permissions
    if not interaction.user.guild_permissions.ban_members:
        # make embed
        embed = discord.Embed(title="Insufficient permissions", description="You do not have permission to use this command", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # ensure the bot has the correct permissions
    if not interaction.guild.me.guild_permissions.ban_members:
        # make embed
        embed = discord.Embed(title="Permission Error", description="I do not have permission to unban users", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # if the user is not banned
    if user not in await interaction.guild.bans():
        # make embed
        embed = discord.Embed(title="Unknown user", description="That user is not banned", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # unban the user
    await interaction.guild.unban(user)
    # send the user a pardon notice
    await user.send("You have been pardoned from " + interaction.guild.name)
    # send the user a confirmation message
    embed = discord.Embed(title="User unbanned", description=f"{user} was unbanned from the server", color=0x2ecc71)
    # send embed
    await interaction.response.send_message(embed=embed)

@bot.command(name="kick", description="Kicks a user from the server")
async def kick(interaction: discord.Interaction, user: discord.User, *, reason: str = None, generate_reason: bool = False):
    # ensure the user has the correct permissions
    if not interaction.user.guild_permissions.kick_members:
        # make embed
        embed = discord.Embed(title="Insufficient permissions", description="You do not have permission to use this command", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # ensure the bot has the correct permissions
    if not interaction.guild.me.guild_permissions.kick_members:
        # make embed
        embed = discord.Embed(title="Permission Error", description="I do not have permission to kick users", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # if the user is not in the server
    if user not in interaction.guild.members:
        # make embed
        embed = discord.Embed(title="Unknown user", description="That user is not in the server", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # if the user is the bot
    if user == interaction.guild.me:
        # make embed
        embed = discord.Embed(title="Self Protection", description="I cannot kick myself", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # if the user is the owner
    if user == interaction.guild.owner:
        # make embed
        embed = discord.Embed(title="Invalid Target", description="I cannot kick the owner", color=0xe74c3c)
        # send embed
        await interaction.response.send_message(embed=embed)
        return
    # if the user is the author
    if user == interaction.user:
        # ask the user if they are sure
        await interaction.response.send_message("Are you sure you want to kick yourself? (y/n)")
        # wait for a response
        response = await bot.wait_for("message", check=lambda message: message.author == interaction.user)
        # if the user is not sure
        if response.content.lower() != "y":
            # make embed
            embed = discord.Embed(title="Cancelled", description="Kick cancelled", color=0xe74c3c)
            # send embed
            await interaction.response.send_message(embed=embed)
            return
    # if the user has higher permissions than the author
    if user.top_role.position > interaction.user.top_role.position:
        # if the user is not the owner
        if user != interaction.guild.owner:
            # make embed
            embed = discord.Embed(title="Insufficient Superiority", description="That user is a higher rank than you", color=0xe74c3c)
            # send embed
            await interaction.response.send_message(embed=embed)
            return
    # if reason is not provided
    if reason is None:
        # set reason to "No reason provided"
        reason = '"No reason provided"'
    # if gererate_reason is true
    if generate_reason:
        embed = discord.Embed(title="Generating reason", description="Please wait while I generate a reason", color=0x3498db)
        # send embed
        await interaction.response.send_message(embed=embed)
        # generate a reason
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="An admin or moderator has requested to kick " + user.name + " from " + interaction.guild.name + ". They supplied this reason as a prompt: "+reason+"\nin less than two sentences tell the user why they were kicked " +user.name+": ",
            n=1,
            max_tokens=200
        )
        # set the reason to the generated reason
        reason = response.choices[0].text
        await user.send(reason)
    else:
        # send the user a kick notice
        await user.send("You have been kicked from " + interaction.guild.name + " for " + reason)
    # kick the user
    await interaction.guild.kick(user, reason=reason)
    # send the user a kick notice

    # edit the embed
    embed = discord.Embed(title="User kicked", description=user.name + " was kicked from the server", color=0x2ecc71)
    # overwrite the embed
    await interaction.edit_original_response(embed=embed)

@bot.command(name="draw", description="Draws an image based on a prompt")
async def drawImage(ctx, prompt: str):
    skipCheck = False

    if isBad(prompt):
        embed = discord.Embed(title="Moderation", description="Your prompt was rejected", color=0xe74c3c)
        await ctx.response.send_message(embed=embed)

    memory = files.loadJson("memory.json")
    try:
        test = memory[str(ctx.user.id)]["allowImage"]
    except:
        memory[str(ctx.user.id)]["allowImage"] = "true"
        memory[str(ctx.user.id)]["imageCount"] = 0
        memory[str(ctx.user.id)]["imageLastUsed"] = "Never"
        files.saveJson("memory.json", memory)
    # check if the user has the allowImage status
    memory = files.loadJson("memory.json")
    now = datetime.datetime.utcnow()
    now = now.strftime("%Y-%m-%d")

    if memory[str(ctx.user.id)]["imageLastUsed"] != now:
        memory[str(ctx.user.id)]["imageCount"] = 0
        memory[str(ctx.user.id)]["allowImage"] = "true"

        files.saveJson("memory.json", memory)
        skipCheck = True

    if memory[str(ctx.user.id)]["allowImage"] == "false" and skipCheck == False:
        embed = discord.Embed(title="Image Limit Reached", description="You have reached the image limit today", color=0xff0000)
        embed.set_footer(text="You can use images again tomorrow")
        await ctx.response.send_message(embed=embed)
        return
    #get the current date
    
    
    
    if memory[str(ctx.user.id)]["imageCount"] >= 25 and skipCheck == False:
        memory[str(ctx.user.id)]["allowImage"] = "false"
        embed = discord.Embed(title="Image Limit Reached", description="You have reached the image limit today", color=0xff0000)
        embed.set_footer(text="You can use images again tomorrow")
        await ctx.response.send_message(embed=embed)
        return
    
    # give the bot the typing status
    async with ctx.channel.typing():
        asyncio.sleep(1)
        # ask the user what they want to draw
    
    
    # wait for a response
    # send the prompt to openai
    async with ctx.channel.typing():
        embed = discord.Embed(title="Please Wait", description="Submitting prompt to OpenAI", color=0x00ff00)
        embed.set_footer(text="This may take a while")
        msg = await ctx.response.send_message(embed=embed)
        await asyncio.sleep(0.2)
        image = await draw(prompt)
        embed = discord.Embed(title="Image Complete", description="Processing image", color=0x00ff00)
        # edit the response
        await msg.edit(embed=embed)
        await asyncio.sleep(1)
        await msg.delete()
        # send the response and reply to the original message
        embed = discord.Embed(title="Image Complete", description="", color=0x00ff00)
        # the image is a url in the variable image
        await msg.edit(embed=embed)
        # send a response that all users can see
        await ctx.response.send_message(file=discord.File(image))
        memory = files.loadJson("memory.json")
        memory[str(ctx.user.id)]["imageCount"] += 1
        memory[str(ctx.user.id)]["defining"] = "false"
        memory[str(ctx.user.id)]["imageLastUsed"] = now
        skipCheck = False
        files.saveJson("memory.json", memory)
    return
#########################################
#                                       #
#   Everything else                     #
#                                       #
#########################################



@client.event
async def on_ready():
    # load the commands from commands.py
    
    print("Connected!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    #if memory.json does not exist, create it
    if not os.path.exists("memory.json"):
        f = open("memory.json", "w")
        f.write("{}")
        f.close()
    
    if not os.path.exists("servers.json"):
        f = open("servers.json", "w")
        f.write("{}")
        f.close()

@client.event
async def on_member_join(member):
    print("Member joined: {}".format(member.name))
    # get their name and the server name
    name = member.name
    server = member.guild.name
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="The user's name is: STAND_IN_NAME>\nThe discord server's name is: " + server + "\nObjective: greet them in a way that does not spark a conversation, use their exact name\nKarmel: ",
        n=1,
        max_tokens=200
    )
    response = response.choices[0].text.replace("STAND_IN_NAME", name)
    # send the response to the server in an embed
    embed = discord.Embed(title=response, description="", color=0x2ecc71)
    # set the image to the user's avatar
    embed.set_thumbnail(url=member.avatar)
    # send the embed and ping the user
    await member.guild.system_channel.send(embed=embed, content=member.mention)

@client.event
async def on_member_remove(member):
    print("Member left: {}".format(member.name))
    # get their name and the server name
    name = member.name
    server = member.guild.name
    # alert the server in an embed
    embed = discord.Embed(title=name + " just left the server", description="", color=0xe74c3c)
    # set the image to the user's avatar
    embed.set_thumbnail(url=member.avatar)
    await member.guild.system_channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    async def fixShitFast():
        memory = files.loadJson("memory.json")
        if str(message.author.id) not in memory: #if the user is not in memory.json yet, add them
            memory[str(message.author.id)] = {}
            memory[str(message.author.id)]["defining"] = "false"
            memory[str(message.author.id)]["imageCount"] = 0
            memory[str(message.author.id)]["allowImage"] = "true"
            memory[str(message.author.id)]["imageLastUsed"] = "0"
            memory[str(message.author.id)]["dmDisclaimer"] = "false"
        try:
            guildName = message.guild.name #get the server name
        except: #if the message is not in a server, it is a DM
            guildName = "DM" #set the server name to DM
        try:
            test = memory[str(message.author.id)]["dmDisclaimer"]
        except:
            memory[str(message.author.id)]["dmDisclaimer"] = "false"

        files.saveJson("memory.json", memory)
        return guildName, memory
    
    guildName, memory = await fixShitFast()

    firstWord = message.content.split()[0].lower()
    
    if client.user.mentioned_in(message):
        await activated(message, isPing=True)

    if firstWord in activate and not client.user.mentioned_in(message):
        await activated(message)

    if guildName == "DM":
        memory = files.loadJson("memory.json")
        if memory[str(message.author.id)]["dmDisclaimer"] != "true":
            embed = discord.Embed(title="Karmel is not meant to be used in DMs", description='Only chat bot actions will be available\nMessages will not require the "Karmel, " prefix\nThis message will not be shown again', color=0xe74c3c)
            await message.channel.send(embed=embed)
            memory[str(message.author.id)]["dmDisclaimer"] = "true"
            files.saveJson("memory.json", memory)
            return
        else:
            await activated(message)

        #if they have not been defined, define them

    
    
client.run(TOKEN)