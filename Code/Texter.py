from discord import Embed
from discord.ext import commands
from config import botKey

bot = commands.Bot(command_prefix='~')

async def messageLoop():
    channelID = input("Channel ID: ")
    channel = bot.get_channel(int(channelID))
    message = input("Message: ")
    try:
        await channel.send(content=message)
        print('Message sent successfully.')
    except Exception:
        print('An error has occurred, message not sent.')
    await messageLoop()

# STARTUP CODE_____________________________________________________________
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await messageLoop()

bot.run(botKey)
