import json
import discord
import requests
import urllib.parse
from config import fortniteAPIKey

# Set Global Variables (Need to be used in 'mode' class and 'getStats')
standardLayout = "Wins: *{wins}*\nWin Rate: *{winRate}%*\nKills: *{kills}*\nK/D: *{kd}*"
divisor = 4


def getStats(epicName, input):

    # Define Variables and Classes
    ptf = ''
    inputType = ''
    img = ''
    errorPNG = "https://i.imgur.com/wunfgw0.png"
    lowerInput = str.lower(input)
    encodedEpicName = urllib.parse.quote(epicName)
    global standardLayout
    global divisor

    class mode():

        def __init__(self, mode, formalName):
            global standardLayout
            global divisor
            self.formalName = formalName
            try:
                self.wins = data['stats'][mode]['top1']['value']
                self.kills = data['stats'][mode]['kills']['value']
                self.winRate = data['stats'][mode]['winRatio']['value']
                self.KD = data['stats'][mode]['kd']['value']
                self.matchCount = data['stats'][mode]['matches']['value']
                self.hasData = True
            except Exception:
                self.wins = 0
                self.kills = 0
                self.winRate = 0
                self.KD = 0
                self.matchCount = 0
                self.hasData = False
                divisor -= 1
            # Has to be set later for self.matchCount to initialize
            self.name = "**{mode}** ({games} matches)".format(
                mode=self.formalName,
                games=self.matchCount
                )

            # Set Embed Values
            if self.hasData is False:
                # No Data Embed
                self.value = ':warning: No data!'
            else:
                # Has Data Embed
                self.value = standardLayout.format(
                    wins=self.wins,
                    winRate=self.winRate,
                    kills=self.kills,
                    kd=self.KD
                    )

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

    # Check Input Type
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
        errorEmbed = discord.Embed(
            title="Error!",
            description="Invalid Input/Console",
            color=0xde2121
            )
        errorEmbed.set_thumbnail(
            url=errorPNG
            )
        errorEmbed.add_field(
            name='Examples:',
            value='switch, pc, touch, etc..',
            inline=True
            )
        return errorEmbed

    # Configure Fortnite Data Request
    requestURL = (
        'https://api.fortnitetracker.com/v1/profile/{pt}/{name}'
        .format(pt=ptf, name=epicName)
        )
    token = fortniteAPIKey

    # Send Request
    request = requests.get(url=requestURL, headers=token)
    data = json.loads(request.text)

    # Check For Valid Username in Response
    try:
        epicUserHandle = data['epicUserHandle']
    except Exception:
        dataEmbed = discord.Embed(
            title="Error!",
            description="Invalid Username",
            color=0xde2121
            )
        dataEmbed.set_thumbnail(
            url=errorPNG
            )
        dataEmbed.add_field(
            name="Command Usage:",
            value='~stats [Epic Username] [Input]',
            inline=True)
        return dataEmbed

# Extract Data From JSON Using 'mode' Class
    solo = mode('p2', 'Solo')
    duo = mode('p10', 'Duo')
    squad = mode('p9', 'Squad')
    ltm = mode('ltm', 'LTM')

    # Configure Embed Layout
    embed = discord.Embed(
        title="Fortnite Stats: {name}"
        .format(name=epicUserHandle),
        url='https://fortnitetracker.com/profile/all/{user}'
        .format(user=encodedEpicName),
        color=0x23b356)
    embed.set_thumbnail(url=img)
    embed.add_field(
        name=solo.name,
        value=solo.value,
        inline=True
    )
    embed.add_field(
        name=duo.name,
        value=duo.value,
        inline=True
    )
    embed.add_field(
        name=squad.name,
        value=squad.value,
        inline=True
    )
    embed.add_field(
        name=ltm.name,
        value=ltm.value,
        inline=True
    )
    embed.add_field(
        name="**All Modes** ({games} matches)".format(
            games = str(int(solo.matchCount)+int(duo.matchCount)+int(squad.matchCount)+int(ltm.matchCount))
        ),
        value=standardLayout.format(
            wins=str(int(solo.wins)+int(duo.wins)+int(squad.wins)+int(ltm.wins)),
            winRate=str(round(((float(solo.winRate)+float(duo.winRate)+float(squad.winRate)+float(ltm.winRate))/divisor), 1)),
            kills=str(int(solo.kills)+int(duo.kills)+int(squad.kills)+int(ltm.kills)),
            kd=str(round(((float(solo.KD)+float(duo.KD)+float(squad.KD)+float(ltm.KD))/divisor), 1)),
            ),
        inline=True
        )
    embed.set_footer(
        text="Input Type: {cont}".format(cont=inputType)
            )

    # Reset Division Multiplier
    divisor = 4

    return embed
