import discord
import traceback
import datetime


async def asyncErr(message, error):
    embed = discord.Embed(title="An error occurred", description="An error occurred while trying to run the command.  Please file a bug report on GitHub.")
    embed.add_field(name="Error", value=error)
    # add a field with a clickable link to the GitHub issues page
    embed.add_field(name="Report a bug", value="https://github.com/OverlordPotato1/Karmel/issues")
    await message.channel.send(embed=embed)

async def defining(id):
    if memory[str(id)]["defining"] == "true":
            return
    
async def hrTime():
    '''
    Gets the time in a human / gpt readable format
    '''
    now = datetime.datetime.now()
    dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week = now.weekday()
    dow = dow[day_of_week]
    day_of_month = now.day
    month = now.month
    year = now.year
    hour = now.hour
    minute = now.minute
    second = now.second
    time = f"{dow} {day_of_month}/{month}/{year} {hour}:{minute}:{second}"
    return time