from src import ChromeDevice, GeoguessrResult, Rules, Time, GeoguessrMap, Challenge, Database, Command, CommandList
import discord
import os.path
import re

device = ChromeDevice('D:/chromedriver.exe')
client = discord.Client()

# Record Tables
db = Database()
db.add_table(Challenge(GeoguessrMap(device, 'famous-places'), Rules.NO_MOVE, time_limit=Time(2, 0)))

# Commands
str_tab = '    '
cm_list = CommandList()
cm_submit = Command('submit', 'Submit a record', 'submit <Game Brakdown URL>|<Game Code>', 'Error submitting')
cm_submitcoop = Command('submitcoop', 'Submit a cooperative record', 'submitcoop <Game Brakdown URL>|<Game Code>', 'Error submitting')
cm_renounce = Command('renounce', 'Renounce a record or cooperative record', 'renounce <Game Brakdown URL>|<Game Code>', 'Error renouncing')
cm_challenge_add = Command('challenge add', 'Add a Challenge or Contest category to the highscores page', 'challenge add point|speed <MapID> default|no_move|no_zoom|no_move_no_zoom|no_move_no_pan_no_zoom no_time_limit|<min>_<sec> <SlotsAvailable=3>', 'Error creating challenge')
cm_help = Command('help', 'Get Help on another command', 'help <Command name>', 'Failed to get help')

cm_list.append(cm_submit)
cm_list.append(cm_submitcoop)
cm_list.append(cm_renounce)
cm_list.append(cm_challenge_add)
cm_list.append(cm_help)


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
    
    sent_message = None
    
    # All Commands
    if content.startswith(cm_list.prefix.strip()):
        sent_message = await message.channel.send("*Processing request...*")
    else:
        return
    
    # Help Command
    if content.startswith(cm_list.prefix + cm_help.command):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_help.token_count
        if len(tokens) != token_count + 1:
            await sent_message.edit(content=cm_help.error + ":\n" + str_tab + cm_help.usage)
            return
        
        for cm in cm_list.list:
            if (cm.command == tokens[token_count]):
                await sent_message.edit(content="**Command Help**:\n" + str_tab + "Name: *" + cm.command + "*\n" + str_tab + "Desc: *" + cm.description + "*\n" + str_tab + "Usage: *" + cm.usage + "*")
                return
        
        await sent_message.edit(content="Unknown Command: *" + tokens[token_count] + "*")
        return
    
    # Submit and SubmitCoop Command
    if content.startswith(cm_list.prefix + cm_submit.command) or content.startswith(cm_list.prefix + cm_submitcoop.command):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_submit.token_count
        if len(tokens) != token_count + 1:
            await sent_message.edit(content=cm_submit.error + ":\n" + str_tab + cm_submit.usage)
            return
        
        code = tokens[token_count].split('/')[-1]
        
        result = None
        try:
            result = GeoguessrResult(device, code)
        except Exception as e:
            await sent_message.edit(content=cm_submit.error + ":\n" + str_tab + str(e))
            return
            
        await sent_message.edit(content="**Submission Accepted!**\nScore: {0}\nDistance: {1}\nTime: {2}\nMap: {3}\nTime Limit: {4}\nRules: {5}".format(
            result.score,
            result.distance,
            result.time,
            result.map,
            result.time_limit,
            result.rules
        ))
        return
    
    # Renounce Command
    if content.startswith(cm_list.prefix + cm_renounce.command):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_renounce.token_count
        if len(tokens) != token_count + 1:
            await sent_message.edit(content=cm_renounce.error + ":\n" + str_tab + cm_renounce.usage)
            return
        
        code = tokens[token_count].split('/')[-1]
        await sent_message.edit(content="**Submission Renonuced!**")
        return
    
    # Challenge Add
    if content.startswith(cm_list.prefix + cm_challenge_add):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_challenge_add.token_count
        if len(tokens) != token_count + 5 or len(tokens) != token_count + 4:
            await sent_message.edit(content=cm_challenge_add.error + ":\n" + str_tab + cm_challenge_add.usage)
            return
            
        max_score_holers = 3
        if len(tokens) == token_count + 5:
            max_score_holers = int(tokens[token_count + 4])
        
        # TODO
        
        await sent_message.edit(content="Challenge Added!")
        return
        
            
        
    
    
    # Invalid Command
    await sent_message.edit(content="Unknown Command: *" + content + "*\n" + str_tab + "Type *" + cm_list.prefix.strip() + "* for a list of commands.")
    

if (os.path.isfile('.token.txt')):
    f = open(".token.txt", "r")
    token = f.read()
    client.run(token)
else:
    client.run(os.environ['TOKEN'])