from json import loads
from discord import Embed
from requests import get
from config import fortniteAPIKey
from BlobheartUserNames import fortniteHandles
from time import sleep


def leaderBoardXPFormat(definedNames):
    if not definedNames:
        nameList = fortniteHandles
    else:
        nameList = definedNames
    scores = (dict(sorted(
        getLeaderBoardXP(nameList).items(),
        key=lambda x: x[1],
        reverse=True
        )))
    names = []
    values = []
    items = scores.items()
    for item in items:
        names.append(item[0]), values.append(item[1])

    scoreEmbed = Embed(
        title="XP Leaderboard",
        color=0x1167b1
    )
    scoreEmbed.set_thumbnail(url='https://i.imgur.com/LIzNl5f.jpg')
    for x in range(len(fortniteHandles)):
        scoreEmbed.add_field(
            name='{num})  **{name}**'.format(
                num=(x+1),
                name=names[x]),
            value='>> ' + ('*{}*'.format('{:,}'.format(values[x]) + ' XP')),
            inline=False
        )

    return scoreEmbed


# Fetches the info for names in nameList and places them in a Dictionary
def getLeaderBoardXP(nameList):
    scoreboard = {}

    def getStats(epicName):
        requestURL = (
            'https://api.fortnitetracker.com/v1/profile/all/{name}'
            .format(name=epicName)
            )
        token = fortniteAPIKey

        request = get(url=requestURL, headers=token)
        data = loads(request.text)

        score = data['lifeTimeStats'][6]['value']
        return int(score.replace(',', ''))

    for x in range(len(fortniteHandles)):
        scoreboard[nameList[x]] = getStats(nameList[x])
        # Sleep To Prevent API From Invalidating Request
        sleep(1)

    return scoreboard
