import discord
import requests
import asyncio
import json


client = discord.Client()

showFiat = False

async def get_price():
    global TokenAddress
    global network
    global showFiat

    url = "https://api.dexscreener.io/latest/dex/pairs/avalanche/0x98d0bdf8745e672a6e2120c492b084230e958304"
    r = requests.get(url)
    json_data = json.loads(r.text)
    print("json_data :")
    print(json_data)
    infos = json_data["pair"]
    print("infos :")
    print(infos)
    if showFiat:
        return infos["priceUsd"]
    else :
        return infos["priceNative"]

async def refreshStatus(): 
    while True:
        prix = await get_price()
        if showFiat:
            symbol = "$"
        else:
            symbol = "AVAX"
        await client.change_presence(activity=discord.Game(name=str(prix) + " " + symbol))
        await asyncio.sleep(5)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(refreshStatus())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if (":crown: Leaders" in [y.name for y in message.author.roles] or "admins" in [x.name.lower() for x in message.author.roles]):
        if message.content.startswith('$showFiat'):
            global showFiat
            showFiat = ~showFiat
            if showFiat :
                await message.channel.send("Showing price in Fiat")
            else :
                await message.channel.send("Showing price in AVAX")
    else :
        await message.channel.send("You need to be a leader or admin to use this command")

client.run('<YOUR DISCORD TOKEN>')
