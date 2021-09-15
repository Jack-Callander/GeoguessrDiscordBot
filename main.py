from src.Challenge import Challenge
from src import ChromeDevice, Distance, GeoguessrMap, GeoguessrResult, Rules, Time, Units
import discord
import os

device = ChromeDevice('D:/chromedriver.exe')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/submit'):
        tokens = message.content.split(' ')
        if len(tokens) == 1:
            # Reply with usage error
            return
            
        result = GeoguessrResult(device, tokens[1])
        await message.channel.send("Submission Accepted!\nScore: {0}\nDistance: {1}\nTime: {2}\nMap: {3}\nTime Limit: {4}\nRules: {5}".format(
            result.score,
            result.distance,
            result.time,
            result.map,
            result.time_limit,
            result.rules
        ))

client.run(os.environ['TOKEN'])