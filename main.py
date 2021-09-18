from frontend import GeoFrontend
from src import ChromeDevice, Database
import discord
import os.path

device = ChromeDevice('D:/chromedriver.exe')
client = discord.Client()

db = Database()
fe = GeoFrontend()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await fe.on_message(message, client, device, db)

if (os.path.isfile('.token.txt')):
    f = open(".token.txt", "r")
    token = f.read()
    client.run(token)
else:
    client.run(os.environ['TOKEN'])