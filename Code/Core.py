from discord import Embed
from discord.ext import commands
from config import botKey
from GetStats import getStats, formatText
from Leaderboard import leaderBoardXPFormat, listMaker
from PrimaryInput import getName, getPrimaryInput
from NNN import leadEmbed, nnnFail, nnnReset
from Fitness import updatePoints, getPoints, fitnessLeaderboard

bot = commands.Bot(command_prefix='~')

# Config Options
debugMessageLog = False


loadingEmbed = Embed(
    title="Loading...",
    description="This will take some time",
    color=0x1167b1)
loadingEmbed.set_thumbnail(url="https://i.imgur.com/Hq39MdR.gif")

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
    loading = await ctx.send(embed=loadingEmbed)
    await ctx.send(embed=leaderBoardXPFormat(definedNames))
    await loading.delete()

@bot.command()
async def input(ctx):
    loading = await ctx.send(embed=loadingEmbed)
    await ctx.send(embed=getPrimaryInput(getName(ctx)))
    await loading.delete()

@bot.command()
async def nnn(ctx):
    await ctx.send(embed=leadEmbed())

@bot.command()
async def nnnfail(ctx):
    await ctx.send(content='{} has failed!'.format(nnnFail(ctx)))
    await ctx.send(embed=leadEmbed())

@bot.command()
async def nnnreset(ctx):
    await ctx.send(content="{}'s status has been restored".format(nnnReset(ctx)))

@bot.command()
async def fitness(ctx):
    notInt = "Sorry, that doesn't look like a valid number... Try running the command again."
    new = ctx.message.content.split(" ")
    try:
        min = int(new[1])
        cal = int(new[2])
    except Exception:
        print(notInt)

    updatePoints(ctx, getPoints(min, cal))
    await ctx.send(embed=fitnessLeaderboard())

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
bot.run(botKey)
