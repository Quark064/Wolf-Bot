from discord import Embed
from datetime import datetime
import json
import os

jsonStorage = os.path.join(os.getcwd(), "Storage", "NNNStorage.json")

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
    nnnStart = datetime(2020, 11, 1)
    time = str((datetime.today())-nnnStart)
    leadEmbed = Embed(title='**NNN Stats** *{}*'.format(time[0:17]), color=0x23b356)
    leadEmbed.set_footer(text="Type '~nnnfail' if you've done the deed")
    for x in range(len(nameList)):
        leadEmbed.add_field(name='**{}**'.format(nameList[str(x)][0]), value=nameList[str(x)][1], inline=True)
    writeJSON(nameList)
    return leadEmbed

def nnnFail(ctx):
    nameList = loadJSON()
    nnnStart = datetime(2020, 11, 1)
    time = str((datetime.today())-nnnStart)
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[str(x)][2]:
            nameList[str(x)][1] = 'Failed, lasted {}'.format(time[0:17])
    writeJSON(nameList)
    return ctx.message.author.mention

def nnnReset(ctx):
    nameList = loadJSON()
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[str(x)][2]:
            nameList[str(x)][1] = 'Passing'
    writeJSON(nameList)
    return ctx.message.author.mention
