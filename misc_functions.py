import discord
import traceback

def logError(error):
    with open("log.txt", "a") as log:
        log.write("\n")
        log.write(error)
        log.write("\n")
        log.write(traceback.format_exc())
        log.write("\n")
        log.write("------------------------------------------------------------")
        log.write("\n")

def logWarn(warning):
    with open("log.txt", "a") as log:
        log.write(warning)
        log.write("\n")

async def asyncErr(message, error):
    embed = discord.Embed(title="An error occurred", description="An error occurred while trying to run the command.  Please file a bug report on GitHub.")
    embed.add_field(name="Error", value=error)
    # add a field with a clickable link to the GitHub issues page
    embed.add_field(name="Report a bug", value="https://github.com/OverlordPotato1/Karmel/issues")
    embed.set_footer(text="Error has been written to the log file")
    try:
        await message.channel.send(embed=embed)
        logError(error)
    except discord.errors.HTTPException:
        embed = discord.Embed(title="An error occurred", description="An error occurred while trying to run the command.  Please file a bug report on GitHub.")
        embed.add_field(name="Error", value="Cannot send error due to HTTPException. Most likely the error is too long. The error has been written to the log file.")
        embed.add_field(name="Report a bug", value="https://github.com/OverlordPotato1/Karmel/issues")
        embed.set_footer(text="what the fuck did you do")
        await message.channel.send(embed=embed)
        # write the error to the log file
        logError(error)