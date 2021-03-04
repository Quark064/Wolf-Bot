import json
import os
from discord import Embed

jsonStorage = os.path.join(os.getcwd(), "Storage", "FitnessStorage.json")

def loadJSON():
    with open(jsonStorage, "r+") as file:
        data = json.load(file)
        return data

def writeJSON(var):
    f = open(jsonStorage, "w")
    f.write(json.dumps(var, indent=4, sort_keys=True))
    f.close()

def updatePoints(ctx, points):
    nameList = loadJSON()
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[str(x)][2]:
            nameList[str(x)][1] += points
            writeJSON(nameList)

def fitnessLeaderboard():
    nameList = loadJSON()
    leadEmbed = Embed(title='**Fitness Leaderboard**', color=0x23b356)
    leadEmbed.set_footer(text="Use ~fitness to add a workout!")

    for x in range(len(nameList)):
        leadEmbed.add_field(name='**{}** - {} Wins'.format(nameList[str(x)][0], nameList[str(x)][3]), value=nameList[str(x)][1], inline=True)

    return leadEmbed

def fitMain(ctx):
    new = ctx.message.content.split(" ")

    try:
        min = int(new[1])
    except Exception:
        ctx.send(content="Sorry, that doesn't look like a valid number... Try running the command again.")
        return

    updatePoints(ctx, (int((min / 700) * 100)))

def fitResetBoard(ctx):
    nameList = loadJSON()
    check = ctx.message.author.mention
    for x in range(len(nameList)):
        if str(check) == nameList[str(x)][2]:
            nameList[str(x)][1] = 0
            writeJSON(nameList)
            return nameList[str(x)][2]
