from discord.ext import commands
from config import botKey
from GetStats import getStats, formatText

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

bot.run(botKey)
