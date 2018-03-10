import discord, asyncio, time, config
from discord.ext import commands
from datetime import datetime
from pytz import timezone

Client = discord.Client()
bot = commands.Bot(command_prefix="-")

players, spect, populate, host = set(), set(), set(), ""
gb_count, inh_time = 0, ""


bot.remove_command('help')


@bot.event
async def on_ready():
    print("Bot is ready!\nSigned in as {0}\nAKA {0}\nUSING BOT TOKEN - {0}".format(bot.user.name, bot.user.id,config.BOT_TOKEN))
    for i in server.Member:
        print(i+"\n")

@bot.event
async def on_member_join(member: discord.Member):
    role = discord.utils.get(member.server.roles, name = "Recruits")
    await bot.add_roles(member,role)
    await bot.send_message(discord.Object(id = config.WELCOME), "Hey, {}! Welcome to the Otters Family, we hope you enjoy your stay. Please let us know which guild you want to join in the <#338181185991606274> channel. Check out <#394771904566919169> , <#339290670520991744> and <#386793544012136449> to know more about the guilds, how to join them and their respective requirements along with the rules that need to be followed! :grin:".format(member.mention))


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
async def inact(cxt, *, args: str):
    if args == None:
        await bot.say("Please provide a proper response. FORMAT: -inact <YOUR IGN> --r <REASON/NOTE FOR BEING INACTIVE>")
    else:
        ex_IGN = args.split('--r')
        IGN = ex_IGN[0]
        if IGN == None or IGN == "":
            await bot.say("Please provide a valid IGN.")
        else:
            ex_RS = ex_IGN[1].split('--d')
            RS = ex_RS[0]
            if RS == None or RS == "":
                await bot.say("Please provide a valid reason for your inactivity.")
            else:
                embed = discord.Embed(title = "INACTIVITY NOTICE", color = 0xd63031)
                embed.add_field(name = "IGN", value = IGN.strip() + " aka " + cxt.message.author.name, inline = True)
                embed.add_field(name = "Reason", value = RS.strip(), inline = False)
                await bot.delete_message(cxt.message)
                await bot.say(cxt.message.author.mention + " - Your inactivity notice has been recorded. I'll let the server mods know about it. Thank you! Arrgh")
                await bot.send_message(discord.Object(id = config.REP_INACT), embed = embed)
                

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
    embed.set_footer(text = "Please contact @BlackClaws or @GhostWings to list your country/Tz.")
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
async def hugs(cxt, *, role: discord.Role = None):
    if role is None:
        await bot.say("Here's a hug for you " + cxt.message.author.mention + ". Forever alone")
    else:
        await bot.say(role.name + ", you guys have been hugged by " + cxt.message.author.mention + " :hugging:")


@bot.command(pass_context=True)
async def pat(cxt, *, member: discord.Member = None):
    if member is None:
        await bot.say("Tag someone to pat them")
    else:
        await bot.say(member.name + ", there there, happens! ***pat pat***")


@bot.command(pass_context = True)
async def announce(cxt, *, message: str = "Nothing to announce"):
    if message == "grind":
        message = "Hey there everyone! The weekend is near, so please get on the grind train and earn hoards of fame points!"
    await bot.send_message(discord.Object(id = config.ANNOUNCE),"@here " + message)


@bot.command(pass_context = True)
async def goodboy(cxt):
    global gb_count
    gb_count += 1
    await bot.say(cxt.message.author.mention + " I'm a good boy! WOOF! [Praise Count = {}]".format(gb_count))


@bot.command(pass_context = True)
async def inhouse_start(cxt, *, time: str = "11:00 PM"):
    global host, inh_time
    inh_time = time
    host = cxt.message.author.mention
    await bot.send_message(discord.Object(id = config.GUILD_PUBLIC), "@here There will be an inhouse today at " + time + " (IST).\n--------------------------------------------------------------------------------------------\n**PLEASE GO TO THE #bot-spam channel and type <--play/spec> to participate**\n--------------------------------------------------------------------------------------------\n")


@bot.command(pass_context = True)
async def play(cxt):
    global players, populate
    if cxt.message.author in populate:
        await bot.say("Your name has already been recorded for the current inhouse session.")
    elif len(players) <= 6:
        players.add(cxt.message.author.mention)
        populate.add(cxt.message.author.mention)
        await bot.say("Hi " + cxt.message.author.mention + ", recorded! Thank you. Current playing capacity: {}/6".format(len(players)))
    else:
        await bot.say("Hi " + cxt.message.author.mention + ", unfortunately the playing party is full! Please try the spec slot or talk to the host.")
            

@bot.command(pass_context = True)
async def spec(cxt):
    global spect, populate
    if cxt.message.author in populate:
        await bot.say("Your name has already been recorded for the current inhouse session.")
    elif len(spect) <= 3:
        spect.add(cxt.message.author.mention)
        populate.add(cxt.message.author.mention)
        await bot.say("Hi " + cxt.message.author.mention + ", recorded! Thank you. Current playing capacity: {}/4".format(len(spect)))
    else:
        await bot.say("Hi " + cxt.message.author.mention + ", unfortunately the spec party is full! Please try the players slot or talk to the host.")


@bot.command(pass_context = True)
@commands.has_role("Elder Treants")
async def inhouse_stop(cxt):
    global players, spect, host
    list_players, list_spec = "", ""
    for i in players:
        list_players += i + "\n"
    for j in spect:
        list_spec += j + "\n"
    embed = discord.Embed(title = "KO - Inhouse | Time - {}".format(inh_time), color = 0xFFFFFF)
    embed.set_footer(text = "@everyone Please go in-game!")
    embed.add_field(name = "Participants", value = list_players, inline = True)
    embed.add_field(name = "Spectators", value = list_spec, inline = True)
    embed.add_field(name = "Host", value = host, inline = True)
    await bot.send_message(discord.Object(id = config.INHOUSE), embed = embed)
    
    players.clear()
    spect.clear()
    host = ""
    

@bot.command(pass_context = True)
@commands.has_role("Elder Treants")
async def kick(cxt, *, member: discord.Member = None):
    ## await bot.send_message(discord.Object(id = config.LOGS), cxt.message.author.mention + " kicked " + member.mention + " :boot:")
    await bot.kick(member)


@bot.command(pass_context = True)
async def role(cxt, *, args: str):
    allowed_roles = (config.ROLES)
    try:
        role_name = args.split(" ")[1]
        role = discord.utils.get(cxt.message.author.server.roles, name = role_name)
        if role.id in allowed_roles:
            await bot.add_roles(cxt.message.author, role)
        else:
            await bot.say("You do not have permission to access that role.")
    except (AttributeError,IndexError):
        await bot.say("Err. Please try again. **Hint: Mention the name of an existing role in this server.**")


##@bot.command(pass_context = True)
##async def dank(cxt):
##    await bot.send_file(cxt.message.channel, 'MMA_Dank.jpg')


def run_bot():
    bot.run(config.BOT_TOKEN)

if __name__ == "__main__": run_bot()
