import discord

def defaultGuild(message):
    guildID = message.guild.id
    guildName = message.guild.name
    guildOwner = message.guild.owner