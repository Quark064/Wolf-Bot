import json
import discord
import requests
import urllib.parse


def getStats(epicName, input):

    ptf = ''
    inputType = ''
    img = ''
    lowerInput = str.lower(input)
    encodedEpicName = urllib.parse.quote(epicName)
    divisor = 4
    noSoloData = False
    noDuoData = False
    noSquadData = False
    noLTMData = False

    contTypes = [
        'switch',
        'xbox',
        'ps',
        'ps4',
        'playstation',
        'gamepad',
        'controller'
        ]
    pcTypes = [
        'pc',
        'computer',
        'keyboard',
        'mouse',
        'kbm'
        ]
    touchTypes = [
        'mobile',
        'phone',
        'touch',
        'android',
        'iphone',
        'ios',
        'samsung',
        'apple'
        ]
    all = [
        'all',
        'everything',
        'everywhere'
    ]

    if lowerInput in contTypes:
        ptf = 'gamepad'
        inputType = 'Controller'
        img = 'https://i.imgur.com/Pk4BypB.png'
    elif lowerInput in pcTypes:
        ptf = 'kbm'
        inputType = 'Mouse and Keyboard'
        img = 'https://i.imgur.com/R4JfrbL.png'
    elif lowerInput in touchTypes:
        ptf = 'touch'
        inputType = 'Touch'
        img = 'https://i.imgur.com/bHiHLXv.png'
    elif lowerInput in all:
        ptf = 'all'
        inputType = 'All'
        img = 'https://i.imgur.com/LIzNl5f.jpg'
    else:
        errorEmbed = discord.Embed()
        errorEmbed = discord.Embed(
            title="Error!",
            description="Invalid Input/Console",
            color=0xde2121
            )
        errorEmbed.set_thumbnail(
            url="https://pluspng.com/img-png/attention-sign-png--2400.png"
            )
        errorEmbed.add_field(
            name='Examples:',
            value='switch, pc, touch, etc..',
            inline=True
            )
        return errorEmbed

    requestURL = (
        'https://api.fortnitetracker.com/v1/profile/{pt}/{name}'
        .format(pt=ptf, name=epicName)
        )
    token = {'TRN-Api-Key': 'bdcb6787-4b1f-4cfe-98db-cb1dde561278'}

    # Send Request
    request = requests.get(url=requestURL, headers=token)
    data = json.loads(request.text)

    try:
        epicUserHandle = data['epicUserHandle']
    except Exception:
        dataEmbed = discord.Embed()
        dataEmbed = discord.Embed(
            title="Error!",
            description="Invalid Username",
            color=0xde2121
            )
        dataEmbed.set_thumbnail(
            url="https://pluspng.com/img-png/attention-sign-png--2400.png"
            )
        dataEmbed.add_field(
            name="Command Usage:",
            value='~stats [Epic Username] [Input]',
            inline=True)
        return dataEmbed

# Extract Data From JSON

    # Solo Stats
    try:
        soloWins = data['stats']['p2']['top1']['value']
        soloKills = data['stats']['p2']['kills']['value']
        soloWinRate = data['stats']['p2']['winRatio']['value']
        soloKD = data['stats']['p2']['kd']['value']
    except Exception:
        noSoloData = True
        soloWins = 0
        soloKills = 0
        soloWinRate = 0
        soloKD = 0
        divisor -= 1

    # Duo Stats
    try:
        duoWins = data['stats']['p10']['top1']['value']
        duoKills = data['stats']['p10']['kills']['value']
        duoWinRate = data['stats']['p10']['winRatio']['value']
        duoKD = data['stats']['p10']['kd']['value']
    except Exception:
        noDuoData = True
        duoWins = 0
        duoKills = 0
        duoWinRate = 0
        duoKD = 0
        divisor -= 1

    # Squad Stats
    try:
        squadWins = data['stats']['p9']['top1']['value']
        squadKills = data['stats']['p9']['kills']['value']
        squadWinRate = data['stats']['p9']['winRatio']['value']
        squadKD = data['stats']['p9']['kd']['value']
    except Exception:
        noSquadData = True
        squadWins = 0
        squadKills = 0
        squadWinRate = 0
        squadKD = 0
        divisor -= 1

    # LTM Stats
    try:
        ltmWins = data['stats']['ltm']['top1']['value']
        ltmKills = data['stats']['ltm']['kills']['value']
        ltmWinRate = data['stats']['ltm']['winRatio']['value']
        ltmKD = data['stats']['ltm']['kd']['value']
    except Exception:
        noLTMData = True
        ltmWins = 0
        ltmKills = 0
        ltmWinRate = 0
        ltmKD = 0
        divisor -= 1

    # Configure Embed Layout
    standardLayout = "Wins: *{wins}*\nWin Rate: *{winRate}%*\nKills: *{kills}*\nK/D: *{kd}*"
    embed = discord.Embed(
        title="Fortnite Stats: {name}"
        .format(name=epicUserHandle),
        url='https://fortnitetracker.com/profile/all/{user}'
        .format(user=encodedEpicName),
        color=0x23b356)
    embed.set_thumbnail(url=img)

    # Solo Data
    if noSoloData is True:
        embed.add_field(
            name="**Solo**",
            value=':warning: No data!',
            inline=True
        )
    else:
        embed.add_field(
            name="**Solo**",
            value=standardLayout
            .format(
                wins=soloWins,
                winRate=soloWinRate,
                kills=soloKills,
                kd=soloKD
                ),
                inline=True
        )

    # Duo Data
    if noDuoData is True:
        embed.add_field(
            name="**Duo**",
            value=':warning: No data!',
            inline=True
        )
    else:
        embed.add_field(
            name="**Duo**",
            value=standardLayout
            .format(
                wins=duoWins,
                winRate=duoWinRate,
                kills=duoKills,
                kd=duoKD
                ),
                inline=True
        )

    # Squad Data
    if noSquadData is True:
        embed.add_field(
            name="**Squad**",
            value=':warning: No data!',
            inline=True
        )
    else:
        embed.add_field(
            name="**Squad**",
            value=standardLayout
            .format(
                wins=squadWins,
                winRate=squadWinRate,
                kills=squadKills,
                kd=squadKD
                ),
                inline=True
        )

    # LTM Data
    if noLTMData is True:
        embed.add_field(
            name="**LTM**",
            value=':warning: No data!',
            inline=True
        )
    else:
        embed.add_field(
            name="**LTM**",
            value=standardLayout
            .format(
                wins=ltmWins,
                winRate=ltmWinRate,
                kills=ltmKills,
                kd=ltmKD
                ),
                inline=True
        )

    embed.add_field(
        name="**All Modes**",
        value=standardLayout
        .format(
            wins=str(int(soloWins)+int(duoWins)+int(squadWins)+int(ltmWins)),
            winRate=str(round(((float(soloWinRate)+float(duoWinRate)+float(squadWinRate)+float(ltmWinRate))/divisor), 1)),
            kills=str(int(soloKills)+int(duoKills)+int(squadKills)+int(ltmKills)),
            kd=str(round(((float(soloKD)+float(duoKD)+float(squadKD)+float(ltmKD))/divisor), 1)),
            ),
        inline=True
        )
    embed.set_footer(
        text="Input Type: {cont}".format(cont=inputType)
            )

    return embed
