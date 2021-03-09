from discord import Embed
from discord.ext import commands
from config import botKey, alphaBotKey
from GetStats import getStats, formatText
from Leaderboard import leaderBoardXPFormat, listMaker
from PrimaryInput import getName, getPrimaryInput
from NNN import leadEmbed, nnnFail, nnnReset, isNov
from Fitness import updatePoints, fitnessLeaderboard, fitMain, fitResetBoard, endSeason
from turtle import ontimer

# Config Options
prefix = '~'
ownerID = '<@285571155950043137>'
debugMessageLog = False
useAlphaBot = False

# Common Assets
loadingEmbed = Embed(
    title="Loading...",
    description="This will take some time",
    color=0x1167b1)
loadingEmbed.set_thumbnail(url="https://i.imgur.com/GX6egvX.gif")

# STARTUP CODE_____________________________________________________________
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# List BOT Commands________________________________________________________

# Fortnite Commands
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
    loading = await ctx.send(embed=loadingEmbed)
    await ctx.send(embed=leaderBoardXPFormat(definedNames))
    await loading.delete()

@bot.command()
async def input(ctx):
    loading = await ctx.send(embed=loadingEmbed)
    await ctx.send(embed=getPrimaryInput(getName(ctx)))
    await loading.delete()

# NNN Commands
@bot.command()
async def nnn(ctx):
    await ctx.send(embed=leadEmbed())

@bot.command()
async def nnnfail(ctx):
    if isNov():
        await ctx.send(content='{} has failed!'.format(nnnFail(ctx)))
    await ctx.send(embed=leadEmbed())

@bot.command()
async def nnnreset(ctx):
    if isNov():
        await ctx.send(content="{}'s status has been restored".format(nnnReset(ctx)))
    await ctx.send(embed=leadEmbed())

# Fitness Challenge Commands
@bot.command()
async def fitness(ctx):
    fitMain(ctx)
    await ctx.send(embed=fitnessLeaderboard())

@bot.command()
async def fitleaderboard(ctx):
    await ctx.send(embed=fitnessLeaderboard())

@bot.command()
async def fitboardreset(ctx):
    await ctx.send(content="{}'s points have been reset!".format(fitResetBoard(ctx)))
    await ctx.send(embed=fitnessLeaderboard())

@bot.command()
async def endseason(ctx):
    if ctx.message.author.mention == ownerID:
        await ctx.send(embed=endSeason())
        await ctx.send(embed=fitnessLeaderboard())
    else:
        await ctx.send(content="You don't have permission to end the season!")


# Other On Message Commands
@bot.event
async def on_message(message):
    if debugMessageLog == True:
        debugMessageLogFunction(message)

    await bot.process_commands(message)


# Function Storage
def debugMessageLogFunction(message):
    try:

        print('{server} > {channel} ({id}) > {user}: {message}'.format(
        server = message.guild,
        channel = message.channel,
        id = message.channel.id,
        user = message.author.name,
        message = message.content
        ))

        for x in range(len(message.attachments)):
            print("\x1b]8;;{link}\a{linkText}\x1b]8;;\a".format(
            link = message.attachments[x].url,
            linkText = "Image {}".format(x)
            ))

    except Exception:
        print('Unknown Message/Error')

# Run
bot.run(alphaBotKey if useAlphaBot == True else botKey)
