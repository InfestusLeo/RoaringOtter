import discord, asyncio, time, config
from discord.ext import commands
from datetime import datetime
from pytz import timezone

Client = discord.Client()
bot = commands.Bot(command_prefix="-")

gb_count, inh_time = 0, ""
inact_token = 0


bot.remove_command('help')


@bot.event
async def on_ready():
    print("Bot is ready!\nSigned in as {0}\nAKA {0}\nUSING BOT TOKEN - {1}".format(bot.user.name, bot.user.id,config.BOT_TOKEN))

@bot.event
async def on_member_join(member: discord.Member):
    dm_message = """\\
Hey, there, welcome to the **Otters Family**, we hope you enjoy your stay! Since you've just joined our server,  you'll have restricted access, meaning you won't be able to access all of the channels. You might want to know how to join us, it's pretty simple!
1. Read the simple requirements for being accepted into one of the guilds: (read full version at **#rules-n-requirements**)
----------------------------------------------------------
REQUIREMENTS FOR KARNIVORE OTTERS
----------------------------------------------------------
- Highest rank achieved of **The Hotness (Tier 7) or above**. Exceptions can be made with tier as it's the start of the season.
- 1700 fame points/week for a temporary spot
- 2000 fame points/week for a permanent spot
----------------------------------------------------------
REQUIREMENTS FOR HERBIVORE OTTERS
----------------------------------------------------------
- Highest rank achieved of **Worthy Foe (Tier 4) or above**. Exceptions can be made with tier as it's the start of the season.
- 1200 fame points/week for a temporary spot
- 1500 fame points/week for a permanent spot
2. Now, let us know your IGN, skill tier and which guild you are looking to join in **#initiation**, by tagging BlackClaws and GhostWings. A member of staff will attend to you soon!
3. While you wait, please read #wiki which includes some helpful tips about using our server. Also, you can hang out in #lounge and talk to other members. :wink:
4. Someone will respond to you soon and arrange an invite to the guild you're looking to join! :smile:
"""
    await bot.send_message(discord.Object(id = config.WELCOME), "Hey, {}! Welcome to the {}, we hope you enjoy your stay. :grin:".format(member.mention, member.server))
    await bot.send_message(member, dm_message)


@bot.command(pass_context = True)
async def kill(cxt, *, member: discord.Member):
    if member == None:
        await bot.say("Whom should I kill?")
    if member.nick == None:
        nick = member.name
    else: nick = member.nick
    
    if nick.startswith('DEAD'):
        await bot.say('The member is already dead! Mwahahahahha!')
    else:
        await bot.say("SLAUGHTERED!")
        await bot.change_nickname(member,"DEAD_" + nick)
        

@bot.command(pass_context = True)
async def act(cxt, *, msg_token: str):
    pass

	
@bot.command(pass_context=True)
async def time(cxt, *, tz: str = ""):
    time_zones = ['Asia/Kolkata', 'Asia/Singapore', 'Asia/Manila', 'Australia/Perth', 'Australia/Queensland','Pacific/Auckland','US/Pacific','Asia/Kathmandu','Asia/Bangkok']
    cities, times = "", ""
    dt_format = "%I:%M %p"
    time = []
    msg, city = "", []
    if tz == "":
        for i in time_zones:
            local_time = datetime.now(timezone(i)).strftime(dt_format)
            city = i.split("/")[1]
            if city == 'Kolkata':
                city += " (IST)"
            if city == 'Pacific':
                city = "Seattle"
            if city == "Bangkok":
                city = "Cambodia"
            cities += city + "\n"
            times += local_time + "\n"
    else:
        msg = datetime.now(timezone(tz)).strftime(dt_format)

    embed = discord.Embed(title = "Time according to various Tz", color = 0xFFFFFF)
    embed.set_footer(text = "Please contact @GhostWings or @BlackClaws to list your country/Tz.")
    embed.add_field(name = "Country/Tz", value = cities, inline = True)
    embed.add_field(name = "Time", value = times, inline = True)
    await bot.say(embed = embed)


@bot.command(pass_context=True)
async def echo(cxt, *, echo: str = "There is nothing for me to say Bakamura."):
    await bot.say(echo)


@bot.command(pass_context=True)
async def hug(cxt, *, member: discord.Member = None):
    if member is None:
        await bot.say("Here's a hug for you " + cxt.message.author.mention + ". Forever alone")
    else:
        await bot.say(member.name + ", you have been hugged by " + cxt.message.author.mention + " :hugging:")

		
@bot.command(pass_context=True)
async def pat(cxt, *, member: discord.Member = None):
    if member is None:
        await bot.say("Tag someone to pat them")
    else:
        await bot.say(member.name + ", there there, happens! ***pat pat***")

    
@bot.command(pass_context = True)
async def goodboy(cxt):
    global gb_count
    gb_count += 1
    await bot.say(cxt.message.author.mention + " I'm a good boy! WOOF! [Praise Count = {}]".format(gb_count))

	
@bot.command(pass_context = True)
@commands.has_role("Elder Treants")
async def kick(cxt, *, member: discord.Member = None):
	pass



bot.run(config.BOT_TOKEN)
