import discord, asyncio, time
from discord.ext import commands
from datetime import datetime
from pytz import timezone

Client = discord.Client()
bot = commands.Bot(command_prefix="!otter ")

players, spec, host = set(), set(), ""

@bot.event
async def on_ready():
    print("Bot is ready!\nSigned in as {0}\nAKA {0}".format(bot.user.name, bot.user.id))


@bot.command(pass_context=True)
async def time(cxt, *, member: discord.Member = None):
    time_zones = ['Asia/Kolkata', 'Asia/Singapore', 'Asia/Manila', 'Australia/Perth', 'Australia/Queensland']
    dt_format = "%I:%M %p"
    time = []
    op, msg, city = [], "", []
    for i in time_zones:
        local_time = datetime.now(timezone(i)).strftime(dt_format)
        city = i.split("/")[1]
        if city == 'Kolkata':
            city += " (IST)"
        msg += city + " - " + local_time + "\n"
    await bot.say(cxt.message.author.mention + "\n" + msg)


@bot.command(pass_context=True)
async def echo(cxt, *, echo: str = "There is nothing for me to say Bakamura."):
    while True:
        await bot.say(echo)
        await asyncio.sleep(2)


@bot.command(pass_context=True)
async def hug(cxt, *, member: discord.Member = None):
    if member is None:
        await bot.say("Here's a hug for you " + cxt.message.author.mention + ". Forever alone")
    else:
        await bot.say(member.mention + ", you have been hugged by " + cxt.message.author.mention)


@bot.command(pass_context = True)
async def announce(cxt, *, announcement: str = "Nothing to announce"):
    if announcement == "grind":
        message = "Hey there everyone! The weekend is near, so please get on the grind train and earn hoards of fame points!"
    await bot.send_message(discord.Object(id="327044820482785300"),"@here " + message)
    
@bot.command(pass_context = True)
async def goodboy(cxt):
    await bot.say(cxt.message.author.mention + " I'm a good boy! WOOF!")

@bot.command(pass_context = True)
async def poll(cxt, *, question: str):
    await bot.say("here " + poll)
    bot.add_reaction("here "+poll,reaction)

@bot.command(pass_context = True)
async def inhouse_start(cxt, *, time: str):
    global host
    host = cxt.message.author.mention
    await bot.send_message(discord.Object(id="366484250155024384"), "There will be an inhouse today at " + time + " (IST).\n--------------------------------------------------------------------------------------------\n**PLEASE GO TO THE #bot-spam channel and type <!otter play/spec> to participate**\n--------------------------------------------------------------------------------------------\n")

@bot.command(pass_context = True)
async def play(cxt):
    global players
    if cxt.message.author.mention in players:
        await bot.say("Your name has already been recorded for the current inhouse. Bakamura.")
    else:
        if len(players) <= 6:
            await bot.say("Hi " + cxt.message.author.mention + ", recorded! Thank you. Current playing capacity: {}/6".format(len(players)))
            players.add(cxt.message.author.mention)
        else:
            await bot.say("Hi " + cxt.message.author.mention + ", unfortunately the playing party is full! Please try the spec slot or talk to the host.")
    host = cxt.message.author.mention

@bot.command(pass_context = True)
async def spec(cxt):
    global spec, host
    spec.add(host)
    if cxt.message.author.mention in players:
        await bot.say("Your name has already been recorded for the current inhouse. Bakamura.")
    else:
        if len(players) <= 4:
            spec.add(cxt.message.author.mention)
            await bot.say("Hi " + cxt.message.author.mention + ", recorded! Thank you. Current playing capacity: {}/6".format(len(players)))
        else:
            await bot.say("Hi " + cxt.message.author.mention + ", unfortunately the spec party is full! Please try the players slot or talk to the host.")

@bot.command(pass_context = True)
async def inhouse_stop(cxt):
    global players, spec, host
    playing, spec = "", ""
    for i in players:
        playing += i + "\n"
    for j in spec:
        spec += j + "\n"
    await bot.send_message(discord.Object(id="401968232203812877"),"KO-Inhouse | HOST - " + host + "\n-----------------------PARTICIPANTS :-----------------------\n" + players + "\n-----------------------SPECTATORS :-----------------------\n" + spec)
    players, spec = set(), set()
    host = ""


bot.run("Mzg3MTM2OTYwMTM5MTAwMTYw.DQbm5g.C-Y0ygbxgH_5SNzfV_VdCqQl8bw")
