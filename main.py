from src.Challenge import Challenge
from src import ChromeDevice, Distance, GeoguessrMap, GeoguessrResult, Rules, Time, Units
import discord
import os
import re

device = ChromeDevice('D:/chromedriver.exe')

client = discord.Client()

class Command:
    def __init__(self, command: str, description: str, usage: str, error: str = "Command error"):
        self.command = command
        self.description = description
        self.usage = usage
        self.error = error
    
    @property
    def token_count(self) -> int:
        return len(self.command.strip().split(' '))

class CommandList:
    def __init__(self):
        self.list = []
        self.prefix = "/geo "
    
    def append(self, cm: Command):
        self.list.append(cm)
    
    def __str__(self) -> str:
        out = "**Command List:**\n"
        for cm in self.list:
            out += "    " + self.prefix + cm.usage + "\n"
        return out
    
    @property
    def token_count(self) -> int:
        return len(self.prefix.strip().split(' '))


# Commands
str_tab = '    '
cm_list = CommandList()
cm_submit = Command('submit', 'Submit a record', 'submit <Game Brakdown URL>|<Game Code>', 'Error submitting')

cm_list.append(cm_submit)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # New Received Message Content
    content = re.sub(r' +', ' ', message.content.strip())
    
    # Command List (produced by only typing the command prefix)
    if content == cm_list.prefix.strip():
        await message.channel.send(cm_list)
        return
    
    # All Commands
    if content.startswith(cm_list.prefix.strip()):
        await message.channel.send("*Processing request...*")
    else:
        return
    
    # Submit Command
    if content.startswith(cm_list.prefix + cm_submit.command):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_submit.token_count
        if len(tokens) != token_count + 1:
            await message.channel.send(cm_submit.error + ":\n" + str_tab + cm_submit.usage)
            return
        
        try:
            result = GeoguessrResult(device, tokens[token_count])
        except Exception as e:
            await message.channel.send(cm_submit.error + ":\n" + str_tab + e)
            return
            
            
        result = GeoguessrResult(device, tokens[token_count])
        await message.channel.send("Submission Accepted!\nScore: {0}\nDistance: {1}\nTime: {2}\nMap: {3}\nTime Limit: {4}\nRules: {5}".format(
            result.score,
            result.distance,
            result.time,
            result.map,
            result.time_limit,
            result.rules
        ))

client.run('ODg3MjU1MTU3ODk5OTIzNTA2.YUBewg.caQmr75n1OJ8W8q8TipFrZfVtUs')
#client.run(os.environ['TOKEN'])