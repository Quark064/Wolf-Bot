from discord import Embed
from discord.ext import commands
from config import botKey
from GetStats import getStats, formatText
from Leaderboard import leaderBoardXPFormat, listMaker, generateErrorEmbed

bot = commands.Bot(command_prefix='~')

# STARTUP CODE_____________________________________________________________
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# List Commands
@bot.command()
async def stats(ctx):
    formatted = formatText(ctx)
    loading = await ctx.send(content='Loading...')
    await ctx.send(embed=getStats(formatted.epicID, formatted.input))
    await loading.delete()


@bot.command()
async def leaderboard(ctx):
    definedNames = []
    definedNames = listMaker(ctx)
    loadingEmbed = Embed(
        title="Loading...",
        description="This will take some time",
        color=0x1167b1)
    loadingEmbed.set_thumbnail(url="https://i.imgur.com/Hq39MdR.gif")
    loading = await ctx.send(embed=loadingEmbed)
    try:
        await ctx.send(embed=leaderBoardXPFormat(definedNames))
        await loading.delete()
    except Exception:
        await ctx.send(embed=generateErrorEmbed)

bot.run(botKey)
