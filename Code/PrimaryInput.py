from config import fortniteAPIKey
from json import loads
from requests import get
from time import sleep
from discord import Embed

epicUserHandle = ''


def getName(ctx):
    str = ctx.message.content.split(' ')
    return(' '.join(str[1:(len(str))]))


def getMatchCount(epicID, inputType):
    requestURL = (
        'https://api.fortnitetracker.com/v1/profile/{input}/{name}'
        .format(input=inputType, name=epicID)
        )
    token = fortniteAPIKey
    global epicUserHandle

    request = get(url=requestURL, headers=token)
    data = loads(request.text)

    matches = data['lifeTimeStats'][7]['value']
    try:
        epicUserHandle = data['epicUserHandle']
    except Exception:
        pass
    return int(matches)


def getPrimaryInput(epicID):
    inputType = ''
    img = ''
    inputDict = {}
    inputTypes = ['touch', 'gamepad', 'kbm']
    errorEmbed = Embed(
            title="Error!",
            description="Invalid Username",
            color=0xde2121
            )
    errorEmbed.set_thumbnail(
            url='https://i.imgur.com/wunfgw0.png'
            )

    for x in range(len(inputTypes)):
        try:
            inputDict[inputTypes[x]] = getMatchCount(epicID, inputTypes[x])
        except Exception:
            inputDict[inputTypes[x]] = 0
        if x < 2:
            sleep(1)

    sortedStats = (dict(sorted(
        inputDict.items(),
        key=lambda x: x[1],
        reverse=True
        )))
    keys = []
    values = []
    items = sortedStats.items()
    for item in items:
        keys.append(item[0]), values.append(item[1])

    totalMatches = 0
    for x in range(len(values)):
        totalMatches += values[x]
    if totalMatches == 0:
        return errorEmbed

    prob = '*{}%*'.format(round(((values[0]/totalMatches)*100), 1))

    if keys[0] == 'touch':
        inputType = 'Touch'
        img = 'https://i.imgur.com/bHiHLXv.png'
    elif keys[0] == 'gamepad':
        inputType = 'Controller'
        img = 'https://i.imgur.com/Pk4BypB.png'
    elif keys[0] == 'kbm':
        inputType = 'Mouse and Keyboard'
        img = 'https://i.imgur.com/R4JfrbL.png'

    inputEmbed = Embed(
        title=epicUserHandle,
        description="Most likely using **{inputType}** ({prob} chance).".format(
            inputType=inputType,
            prob=prob
        ),
        color=0x8f118b
        )
    inputEmbed.set_thumbnail(
        url=img
        )

    return inputEmbed
