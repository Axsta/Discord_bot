import discord
import asyncio
import datetime
import re
import ffmpeg
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import os
from profanity_check import predict, predict_prob

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
intents.members = True

bot = commands.Bot(command_prefix="|", intents=intents)
bot.remove_command('help')



@bot.event
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
    embed1.add_field(name="|help", value="This command provides information about every other command", inline=False)
    embed1.add_field(name="hello/hey/hi", value="This command greets the user", inline=False)
    embed1.add_field(name="|users", value="This command tells you the name and size of the server", inline=False)
    embed1.add_field(name="|help_sound", value="This command greets the user", inline=False)
    embed1.set_footer(text="Lastly,the bot filters out bad words in the server and you cant change your nickname to my name 'pink'. More actions will be added soon!")
    await member.guild.system_channel.send(embed=embed1)


@bot.event
async def on_guild_join(guild):
    """
    this is the joining message when the bot is added to the bot
    """

    if guild.system_channel:  # If it is not None
        await guild.system_channel.send(f'Thanks for inviting me to {guild.name}')


@bot.event
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

@bot.command(name="play")
async def play(ctx, arg):
    def operations(arg):
        switch = {
            'clip1': 'audio_clips/Misc_soundboard_brutal.mp3.mpeg',
            'clip2': 'audio_clips/Misc_soundboard_ding_ding_ding.mp3.mpeg',
            'clip3': 'audio_clips/Misc_soundboard_disastah.mp3.mpeg',
            'clip4': 'audio_clips/Misc_soundboard_easiest_money.mp3.mpeg',
            'clip5': 'audio_clips/Misc_soundboard_looking_spicy.mp3.mpeg',
            'clip6': 'audio_clips/Misc_soundboard_next_level.mp3.mpeg',
            'clip7': 'audio_clips/Misc_soundboard_ni_qi_bu_qi.mp3.mpeg',
            'clip8': 'audio_clips/Misc_soundboard_ta_daaaa.mp3.mpeg',
            'clip9': 'audio_clips/Misc_soundboard_ti9_kooka_laugh.mp3.mpeg',
            'clip10': 'audio_clips/Misc_soundboard_what_just_happened.mp3.mpeg',
            'clip11': 'audio_clips/Misc_soundboard_whats_cooking.mp3.mpeg',
            'clip12': 'audio_clips/Misc_soundboard_wow.mp3.mpeg',
            'clip13': 'audio_clips/Misc_soundboard_youre_a_hero.mp3.mpeg',
            'clip14': 'audio_clips/Misc_soundboard_no_chill.mp3.mpeg'
        }
        return switch.get(arg, "Not defined")

    audio_source = discord.FFmpegPCMAudio(operations(arg))
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return

    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

    server = ctx.message.guild
    voice_client = server.voice_client
    
    if ctx.message.author.voice:
            async with ctx.typing():
                        voice_client.play(audio_source, after=None)


    while voice_client.is_playing():
        await asyncio.sleep(1)
    else:
        await voice_client.disconnect()
        print("Disconnected")


@bot.command(name="help_sound")
async def on_message(ctx):
    embed2 = discord.Embed(title="How to use the chat clips?", description="Type |play followed by the clip number",
                           url="https://discord.gg/tAEvRZ4Dy7", color=0xFF5733)
    embed2.add_field(name='clip1', value="Brutal. Savage. Rekt.", inline=False)
    embed2.add_field(name='clip2', value="Ding Ding Ding Mother******", inline=False)
    embed2.add_field(name='clip3', value="It's a disastah!", inline=False)
    embed2.add_field(name='clip4', value="Easiest money of my life!", inline=False)
    embed2.add_field(name='clip5', value="It's looking Spicy!.", inline=False)
    embed2.add_field(name='clip6', value="The next level play!", inline=False)
    embed2.add_field(name='clip7', value="你气不气？", inline=False)
    embed2.add_field(name='clip8', value="Lakad Matataaag! Normalin, Normalin.", inline=False)
    embed2.add_field(name='clip9', value="Kookabura Laugh", inline=False)
    embed2.add_field(name='clip10', value=" I can't believe what we're seeing. What just happened?", inline=False)
    embed2.add_field(name='clip11', value="You know what's cooking? BOOM!", inline=False)
    embed2.add_field(name='clip12', value="Waow", inline=False)
    embed2.add_field(name='clip13', value="You're a goddamn hero!", inline=False)
    embed2.add_field(name='clip14', value=" This guy has no chill", inline=False)

    await ctx.send(embed=embed2)                  

@bot.command(name='users')
async def fetchServerInfo(ctx):
    guild = ctx.guild
    await ctx.send(f'Server Name: {guild.name}')
    await ctx.send(f'Server Size: {(guild.member_count)}')
    
    
@bot.event
async def on_message(message):
    global messages
    messages += 1

    channel = []  # change v2
    invalid_user = ["Mildly Irritated Bot#2847"]
    words = [message.content]

    # filters out the specified bad words from the channel
    if predict(words) == 1:
        await message.delete()

    # displays help content with instructions for each actions
    if message.content == "|help":
        embed = discord.Embed(title="How to use the Cat Bot?", description="This is the official bot for the channel",
                              url="https://discord.gg/tAEvRZ4Dy7", color=0xFF5733)
        embed.add_field(name="|help", value="This command provides information about every other command", inline=False)
        embed.add_field(name="hello/hey/hi", value="This command greets the user", inline=False)
        embed.add_field(name="|users", value="This command tells you the name and size of the server", inline=False)
        embed.add_field(name="|help_sound", value="This command greets the user", inline=False)
        embed.set_footer(text="Lastly,the bot filters out bad words in the server and you cant change your nickname to my name 'pink'. More actions will be added soon!")
        await message.channel.send(embed=embed)

    # change v2
    if str(message.author) not in invalid_user:
        # responds to greetings
        if re.search(r"\b(hello|hi|hey)\b", message.content, flags=re.IGNORECASE):
            await message.channel.send(f"""Hi {message.author.mention}""")

    else:
        # maintains log of user actions that did not get executed by the bot
        print(f"""User: {message.author} tried to do the command {message.content}, in channel {message.channel}""")



bot.loop.create_task(update_stats())
bot.run(token)
