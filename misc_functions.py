import discord
import traceback


async def asyncErr(message, error):
    embed = discord.Embed(title="An error occurred", description="An error occurred while trying to run the command.  Please file a bug report on GitHub.")
    embed.add_field(name="Error", value=error)
    # add a field with a clickable link to the GitHub issues page
    embed.add_field(name="Report a bug", value="https://github.com/OverlordPotato1/Karmel/issues")
    await message.channel.send(embed=embed)