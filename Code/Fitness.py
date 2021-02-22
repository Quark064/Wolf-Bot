from discord import Embed

nameList = {
  0: ["Will", 0,"<@285571155950043137>"],
  1: ["Jasmine", 0,"<@418901709713178634>"],
  2: ["Ta'Mariah", 0,"<@562762988571066368>"]
}


def updatePoints(ctx, points):
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[x][2]:
            nameList[x][1] += points

def getPoints(min, cal):
    calPoints = int((cal / 700) * 100)
    minPoints = int((min / 30) * 100)
    return (calPoints + minPoints)

def fitnessLeaderboard():
    leadEmbed = Embed(title='**Fitness Leaderboard**', color=0x23b356)
    leadEmbed.set_footer(text="Use ~fitness to add a workout!")
    for x in range(len(nameList)):
        leadEmbed.add_field(name='**{}**'.format(nameList[x][0]), value=nameList[x][1], inline=True)
    return leadEmbed
