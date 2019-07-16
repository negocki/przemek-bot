import discord
import asyncio
from discord.ext import commands
import random
import sqlite3

from cytaty import Cytaty
from wykop_features import WykopFeatures
from minus5 import Minus5
from datetime import datetime

client = discord.Client()
conn = sqlite3.connect('discobot.db')

cytat = Cytaty(conn)
wykop = WykopFeatures()
minus5 = Minus5(conn)

startup_time = datetime.now()


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Spierdalaj {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!help'):
        msg = '```Lista komend:\n!wykop - losowy wpis z gorących mirko \n!cytat - losowy cytat \n!cytat [numer] - konkretny cytat \n!addcytat - dodawanie cytatu \n!topminus5```'
        await message.channel.send(msg)

    if message.content.startswith('!wykop'):  # mirko
       entry = wykop.get_random_hot()
       msg = '```@{} - {} - {} głosów```\n{}'.format(entry[1],entry[4],entry[3],entry[5])
       await message.channel.send(msg)

    if message.content.startswith('!bachu'):
        msg = 'http://i.imgur.com/lOx73f1.jpg'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!goha'):
        msg = 'go ha go ha go ha go ha 3 zł'.format(message)
        await message.channel.send(msg)
        #await client.send_message(message.channel, msg, tts=True)

    if message.content.startswith('!pszemek'):
        msg = 'https://cdn.discordapp.com/attachments/338355995124301824/353985149890854912/DSC_0160.JPG'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!makaron'):
        msg = 'https://cdn.discordapp.com/attachments/355434446398160897/355435945824092161/ZVKjmto.jpg'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!addcytat'):  # dodawanie cytatu

        cytat_n = ("","")
        async for message_log in message.channel.history(limit=100): # odczytujemy poprzednia wiadomosc
            if message_log.author != client.user and message_log.author != message.author:
                cytat_n = (message_log.author, message_log.content)
                break
        cytat.dodaj_cytat(cytat_n[0],cytat_n[1])

    if message.content.startswith('!cytat'):
        cytat_g =""
        if(len(message.content) > 6):  # czy podano numer cytatu
            numer_cytatu = int(message.content[7:])
            cytat_g = cytat.cytat(numer_cytatu)
        else:
            cytat_g = cytat.losuj_cytat()

        if cytat_g != (0,0,0):
            msg = 'Cytat: {} {} powiedział \n "{}"'.format(cytat_g[2],cytat_g[0],cytat_g[1])
        else:
            msg = 'Nie znaleziono cytatu'

        await message.channel.send(msg)

    if message.content.startswith('!topminus5'):
        stats = sorted(minus5.get_stats(), key=lambda x: x[1], reverse=True)
        msg = 'Statystyki obrażania matek:\n'
        for user_id, count in stats:
            user_data = await client.fetch_user(user_id)
            msg += user_data.display_name + ': ' + str(count * -5) + ' punktów\n'

        await message.channel.send(msg)

    #recalc sie sypie, niech ktos
    # if message.content.startswith('!recalcminus5') and (message.author.name == "negocki" or message.author.name == "Kristopher38" or message.author.name == "w0jt1"):
    #     print('Recalculating minus5 stats, this might take a while')
    #     messages = []
    #     recalc_stats = {}
    #
    #     for channel in client.get_all_channels():
    #         # channel_logs = client.logs_from(channel, limit=10000, before=startup_time) # hardcoded 10k messages limit #drugi error
    #         # channel_logs = await channel.history(limit=123).flatten()  # hardcoded 10k messages limit #tu jest blad
    #         # async for msg in channel_logs:
    #         messages = await channel.history(limit=123).flatten()
    #         async for msg in messages:
    #             for reaction in msg.reactions:
    #                 if reaction.custom_emoji:
    #                     if reaction.emoji.name == "minus5":
    #                         if msg.author.id in recalc_stats:
    #                             recalc_stats[msg.author.id] += reaction.count
    #                         else:
    #                             recalc_stats[msg.author.id] = reaction.count
    #
    #     minus5.recalculate_stats(recalc_stats)
    #     print('Recalculating finished')
    #     await message.channel.send('Recalculating finished')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name="!help"))

@client.event
async def on_reaction_add(reaction, user):
    if reaction.custom_emoji:
        if reaction.emoji.name == "minus5":
            minus5.increment_user(reaction.message.author)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.custom_emoji:
        if reaction.emoji.name == "minus5":
            minus5.decrement_user(reaction.message.author)

client.run('')



