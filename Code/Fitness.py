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
        if nameList[str(x)][3] == 1:
            suf = ""
        else:
            suf = "s"
            
        leadEmbed.add_field(name='**{}** - {} Win{}}'.format(nameList[str(x)][0], nameList[str(x)][3], suf), value=nameList[str(x)][1], inline=True)

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

def endSeason():
    nameList = loadJSON()
    max = 0
    winningID = 0
    for x in range(len(nameList)):
        if nameList[str(x)][1] > max:
            max = nameList[str(x)][1]
            winningID = str(x)
        nameList[str(x)][1] = 0

    nameList[winningID][3] += 1

    winEmbed = Embed(title="**Congratualtions!**", color=0xede353)
    winEmbed.set_thumbnail(url="https://i.imgur.com/JD84hdS.png")
    winEmbed.add_field(name="Congrats to {} for winning this season!".format(nameList[winningID][0]), value="The next season starts now, good luck!")

    writeJSON(nameList)
    return winEmbed
