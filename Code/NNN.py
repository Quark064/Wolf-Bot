from discord import Embed
from datetime import datetime

nameList = {
  0: ['Jaygo','Passing','<@265265506309636096>'],
  1: ['Kalif','Passing','<@218667824250355713>'],
  2: ['Jon','Passing','<@261888549257871362>'],
  3: ['Shovel','Passing','<@257967334528909325>'],
  4: ['Sandcheese','Passing','<@306239951547138049>'],
  5: ['Will','Passing','<@285571155950043137>'],
  6: ['James','Passing','<@128258915417849856>'],
  7: ['Hilco','Passing','<@173545217486487552>'],
  8: ['Toby','Passing','<@146656795421573120>'],
  9: ['Tedi','Passing','<@254622654189797376>']
}

def leadEmbed():
    leadEmbed = Embed(title='**NNN Stats**', color=0x23b356)
    for x in range(len(nameList)):
        leadEmbed.add_field(name='**{}**'.format(nameList[x][0]), value=nameList[x][1], inline=True)
    return leadEmbed

def nnnFail(ctx):
    nnnStart = datetime(2020, 11, 1)
    time = str((datetime.today())-nnnStart)
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[x][2]:
            nameList[x][1] = 'Failed, lasted {}'.format(time[0:17])
    return ctx.message.author.mention

def nnnReset(ctx):
    for x in range(len(nameList)):
        if str(ctx.message.author.mention) == nameList[x][2]:
            nameList[x][1] = 'Passing'
    return ctx.message.author.mention
