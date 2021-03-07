from discord import Embed
from datetime import datetime
import json
import os

jsonStorage = os.path.join(os.getcwd(), "Storage", "NNNStorage.json")

class homebrewTime():
    def __init__(self, timedelta):
        self.days = timedelta.days
        self.hours = int((timedelta.seconds / 3600))
        self.minutes = int((timedelta.seconds - (self.hours * 3600)) / 60)
        self.seconds = int(timedelta.seconds - ((self.hours * 3600) + (self.minutes * 60)))

def isNov():
    if datetime.today().month != 11:
        return False
    else:
        return True

def loadJSON():
    with open(jsonStorage, "r+") as file:
        data = json.load(file)
        return data

def writeJSON(var):
    f = open(jsonStorage, "w")
    f.write(json.dumps(var))
    f.close()

def leadEmbed():
    nameList = loadJSON()
    nnnStart = datetime((datetime.today().year), 11, 1)
    today = datetime.today()
    time = homebrewTime(datetime.today()-nnnStart)

    if isNov():
        leadEmbed = Embed(title='**NNN Stats** *{} days, {:02d}:{:02d}:{:02d}*'.format(time.days, time.hours, time.minutes, time.seconds), color=0x23b356)
        leadEmbed.set_footer(text="Type '~nnnfail' if you've done the deed")
    else:
        leadEmbed = Embed(title="**It's not November yet!**", color=0xed0e4d)
        leadEmbed.set_footer(text="Enjoy it while you can...")
        return leadEmbed

    for x in range(len(nameList)):
        leadEmbed.add_field(name='**{}**'.format(nameList[str(x)][0]), value=nameList[str(x)][1], inline=True)

    writeJSON(nameList)
    return leadEmbed

def nnnFail(ctx):
    nameList = loadJSON()
    nnnStart = datetime((datetime.today().year), 11, 1)
    time = homebrewTime(datetime.today()-nnnStart)

    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[str(x)][2]:
            nameList[str(x)][1] = 'Failed, lasted {} days, {:02d}:{:02d}:{:02d}'.format(time.days, time.hours, time.minutes, time.seconds)

    writeJSON(nameList)
    return ctx.message.author.mention

def nnnReset(ctx):
    nameList = loadJSON()

    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[str(x)][2]:
            nameList[str(x)][1] = 'Passing'

    writeJSON(nameList)
    return ctx.message.author.mention
