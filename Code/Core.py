import discord
from GetStats import getStats
from config import botKey


client = discord.Client()

# STARTUP CODE_____________________________________________________________
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Start the Bot
@client.event
async def on_message(message):

    # Check if bot sent message.
    if message.author == client.user:
        return
# _________________________________________________________________________

# Check for Identification Mark
    if message.content.startswith('~'):
        # Run Functions
        if message.content.startswith('~stats'):
            splitstr = message.content.split(' ')
            length = len(splitstr)
            epicID = (' '.join(splitstr[1:(length)-1]))
            input = (''.join(splitstr[(length-1):length]))

            loading = await message.channel.send(content='Loading...')
            await message.channel.send(embed=getStats(epicID, input))
            await loading.delete()
client.run(botKey)
