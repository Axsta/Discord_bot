import discord
import asyncio
import datetime
import re

messages = 0
joined = 0

def read_id():
    """
    reads the server id for the bot for the bot to connect to the server
    """
    with open("server_id.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

id1 = read_id()



def read_token():
    """
    reads the token id for the bot to connect to the code
    """
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()

async def update_stats():
    """
    maintains the server logs
    """
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {str(datetime.datetime.now())}, Messages: {messages}, Joined: {joined} \n")
                messages = 0
                joined = 0

                await asyncio.sleep(300)

        except Exception as e:
            print(e)
            await asyncio.sleep(300)



#setting member intents to receive member events
intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)



@client.event
async def on_member_join(member):
    """
    this is the joining message when member joins the server
    """
    global joined
    joined += 1
    await member.guild.system_channel.send(f"Why are you here {member.mention}? \n ")
    await member.guild.system_channel.send("https://c.tenor.com/tAkRmpf8yTAAAAAC/whats-was-the-reason.gif")
    embed1 = discord.Embed(title="How to use the Cat Bot?", description="This is the official bot for the channel",
                          url="https://discord.gg/tAEvRZ4Dy7", color=0xFF5733)
    embed1.add_field(name="help", value="This command provides information about every other command", inline=False)
    embed1.add_field(name="hello/hey/hi", value="This command greets the user", inline=False)
    embed1.add_field(name="users", value="This command gives the count of members in the server", inline=False)
    embed1.set_footer(text="Lastly,the bot filters out bad words in the server. More actions will be added soon!")
    await member.guild.system_channel.send(embed=embed1)

@client.event
async def on_guild_join(guild):
    """
    this is the joining message when the bot is added to the bot
    """
    if guild.system_channel: # If it is not None
        await guild.system_channel.send(f'Thanks for inviting me to {guild.name}')



@client.event
async def on_member_update(before, after):
    """
    undo the changes to the nickname
    """
    n = after.nick
    if n:
        if n.lower().count("pink") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
               await after.edit(nick="NO STOP THAT")


@client.event

async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(int(id1))
    channel = ["bot_test","welcome"]
    invalid_user = ["Mildly Irritated Bot#2847"]
    bad_words = ["stop", "kill", "suicide", "die"]

    # filters out the specified bad words from the channel
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.delete()
            await message.channel.send(f"A bad word was said by {message.author}")

    # displays help content with instructions for each actions
    if message.content == "help":
        embed = discord.Embed(title="How to use the Cat Bot?", description="This is the official bot for the channel",
                              url="https://discord.gg/tAEvRZ4Dy7", color=0xFF5733)
        embed.add_field(name="help", value="This command provides information about every other command", inline=False)
        embed.add_field(name="hello/hey/hi", value="This command greets the user", inline=False)
        embed.add_field(name="users", value="This command gives the count of members in the server", inline=False)
        embed.set_footer(text="Lastly,the bot filters out bad words in the server. More actions will be added soon!")
        await message.channel.send(embed=embed)



    if str(message.channel) in channel and str(message.author) not in invalid_user:
        # responds to greetings
        if re.search(r"\b(hello|hi|hey)\b", message.content, flags=re.IGNORECASE) :
            await message.channel.send(f"""Hi {message.author.mention}""")

        elif message.content == "users":
            # provide count of users in the channel
            await message.channel.send(f"""Number of members on this server: {id.member_count}""")

    else:
        # maintains log of user actions that did not get executed by the bot
        print(f"""User: {message.author} tried to do the command {message.content}, in channel {message.channel}""")



client.loop.create_task(update_stats())
client.run(token)
