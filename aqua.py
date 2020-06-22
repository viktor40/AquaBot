# aqua.py
# https://discord.com/api/oauth2/authorize?client_id=708960206163411025&permissions=8&scope=bot

import discord
from discord.ext import commands
import random
import time
from dotenv import load_dotenv  # load module for usage of a .env file
import os  # import module for directory management

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id's that have to be kept secret for security
TOKEN = os.getenv('DISCORD_TOKEN')  # get our discord bot token from .env
bot = commands.Bot(command_prefix='aq!')

time_of_msg = 0

# hammer server ID and both aquas client IDs
Hammer_server_ID = 645464470633840651
real_aqua_ID = 504195343265693706
bot_aqua_ID = 708960206163411025


# print a message if the bot is online
@bot.event
async def on_ready():
    print('bot connected')
    # use the global variable time_of_msg and set it to 0 so hammer doesn't get spammed constantly by the bot
    global time_of_msg
    time_of_msg = time.time()
    # change status to being gay
    await bot.change_presence(activity=discord.Game("Being Gay"))


@bot.event
async def on_message(message):
    # don't answer to the ourselves
    if message.author.id == bot.user.id:
        return

    # if someone pings the bot, redirect them to aqua
    if bot.get_user(bot_aqua_ID) in message.mentions:
        response = 'you pinged the wrong one, <@{}> get your gay ass over here'.format(real_aqua_ID)
        await message.channel.send(response)

    # check if the message is in hammer and check the timer
    if message.guild.id == Hammer_server_ID:
        global time_of_msg
        if time.time() - time_of_msg > 600:
            time_of_msg = time.time()
        else:
            return

    # all different forms of I am
    cases = ['I\'m', 'i\'m', 'I am', 'i am', 'Im', 'im']

    # all different things to call aqua
    call_aqua = ['Aqua', 'gay', 'UwUa', 'lesbi-ish']

    # lazy code here, cba to not use try and except
    # if aqua has a nickname in the server it can also use that in call_aqua
    try:
        aqua_nick = message.guild.get_member(real_aqua_ID).display_name
        call_aqua.append(aqua_nick)
    except:
        pass

    # remove the @ from @ messages so it can't be used for pingspam
    if '@' in message.content:
        message.content = message.content.replace('@', '')

    # cycle through the message and check for every case
    for case in cases:
        # in brackets is an escape character here so it won't reply to that
        if '"{}"'.format(case) in message.content:
            return

        # reply something different to I am dumb
        elif '{} dumb'.format(case) in message.content:
            response = 'me too'
            await message.channel.send(response, delete_after=15)
            return

        # reply back to the sender
        elif '{} '.format(case) in message.content:
            response = 'hi {}, I\'m {}!'.format(message.content.split('{} '.format(case))[-1], random.choice(call_aqua))
            print(message.author)
            await message.channel.send(response, delete_after=15)
            return

    await bot.process_commands(message)


# command to test if the bot is running
@bot.command(name='test', help='test if the bot is working')
async def test(ctx):
    response = 'Don\'t worry, I\'m working!'
    await ctx.send(response)


bot.run(TOKEN)
