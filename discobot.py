import discord
import asyncio
from discord.ext import commands
import random
import sqlite3
from cytaty import Cytaty
from wykop_features import WykopFeatures

client = discord.Client()
conn = sqlite3.connect('discobot.db')
cytat = Cytaty(conn)
wykop = WykopFeatures()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Spierdalaj {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!help'):
        msg = 'Lista komend:\n!wykop - losowy wpis z gorących mirko \n !cytat - losowy cytat \n !cytat [numer] - konkretny cytat \n !addcytat - dodawanie cytatu'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!wykop'):  # mirko
        entry = wykop.get_random_hot()
        msg = '```@{} - {} - {} głosów```\n{}'.format(entry[1],entry[4],entry[3],entry[5])
        await client.send_message(message.channel, msg)

    if message.content.startswith('!bachu'):
        msg = 'http://i.imgur.com/lOx73f1.jpg'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!goha'):
        msg = 'go ha go ha go ha go ha 3 zł'.format(message)
        await client.send_message(message.channel, msg, tts=True)

    if message.content.startswith('!pszemek'):
        msg = 'https://cdn.discordapp.com/attachments/338355995124301824/353985149890854912/DSC_0160.JPG'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!makaron'):
        msg = 'https://cdn.discordapp.com/attachments/355434446398160897/355435945824092161/ZVKjmto.jpg'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!addcytat'):  # dodawanie cytatu

        cytat_n = ("","")
        async for message_log in client.logs_from(message.channel, limit=100): # odczytujemy poprzednia wiadomosc
            if message_log.author != client.user and message_log.author != message.author:
                cytat_n = (message_log.author, message_log.content)
                break
        cytat.dodaj_cytat(cytat_n[0],cytat_n[1])

    if message.content.startswith('!cytat'):
        cytat_g = ""
        if(len(message.content) > 6):  # czy podano numer cytatu
            numer_cytatu = int(message.content[7:])
            cytat_g = cytat.cytat(numer_cytatu)
        else:
            cytat_g = cytat.losuj_cytat()

        if cytat_g != (0,0,0):
            msg = 'Cytat: {} {} powiedział \n "{}"'.format(cytat_g[2],cytat_g[0],cytat_g[1])
        else:
            msg = 'Nie znaleziono cytatu'

        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    playing = discord.Game(name="!help")
    await client.change_presence(game=playing)

client.run('MzU1NDMyNTY2ODIxNjE3Njc1.DJMt-Q.FKP0s7QFgcHnCKd8kHODwMqe3hk')