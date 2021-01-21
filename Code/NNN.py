from discord import Embed
from datetime import datetime

nameList = {
  0: ['Jaygo','Passing','<@265265506309636096>'],
  1: ['Kalif','Passing','<@218667824250355713>'],
  2: ['Jon','Never Started','<@261888549257871362>'],
  3: ['Shovel','Failed, lasted 19 days, 18:46:50','<@257967334528909325>'],
  4: ['Sandcheese','Failed, lasted 12 days, 14:48:29','<@306239951547138049>'],
  5: ['Will','Failed, lasted 3 days, 10:18:47','<@285571155950043137>'],
  6: ['James','Passing','<@128258915417849856>'],
  7: ['Hilco','Passing','<@173545217486487552>'],
  8: ['Toby','Passing','<@146656795421573120>'],
  9: ['Tedi','Passing','<@254622654189797376>'],
  10: ['Lux','Passing','<@146025583132934144>'],
  11: ['Gwen','Immune','<@510294568093089793>']
}

def leadEmbed():
    nnnStart = datetime(2020, 11, 1)
    time = str((datetime.today())-nnnStart)
    leadEmbed = Embed(title='**NNN Stats** *{}*'.format(time[0:17]), color=0x23b356)
    leadEmbed.set_footer(text="Type '~nnnfail' if you've done the deed")
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
