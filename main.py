from src import ChromeDevice, GeoguessrResult, Rules, Time, GeoguessrMap, Challenge, Database, Command, CommandList
import discord
import os.path
import re

device = ChromeDevice('D:/chromedriver.exe')
client = discord.Client()

# Record Tables
db = Database()

# Commands
str_tab = '    '
cm_list = CommandList()
cm_submit = Command('submit', 'Submit a record', 'submit <Game Brakdown URL>|<Game Code>', 'Error submitting')
cm_submitcoop = Command('submitcoop', 'Submit a cooperative record', 'submitcoop <Game Brakdown URL>|<Game Code>', 'Error submitting')
cm_renounce = Command('renounce', 'Renounce a record or cooperative record', 'renounce <Game Brakdown URL>|<Game Code>', 'Error renouncing')
cm_challenge = Command('challenge', 'Add or Remove a Challenge or Contest category to the highscores page', 'challenge add|remove point|speed <MapID> default|no-move|no-zoom|no-move-no-zoom|no-move-no-pan-no-zoom no-time-limit|<min>-<sec> [SlotsAvailable=3]', 'Error creating challenge')
cm_help = Command('help', 'Get Help on another command', 'help <Command name>', 'Failed to get help')

cm_list.append(cm_submit)
cm_list.append(cm_submitcoop)
cm_list.append(cm_renounce)
cm_list.append(cm_challenge)
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
        result = GeoguessrResult(device, code)
        
        try:
            await sent_message.edit(content="**Submission Accepted!**\nScore: {0}\nDistance: {1}\nTime: {2}\nMap: {3}\nTime Limit: {4}\nRules: {5}".format(
                result.score,
                result.distance,
                result.time,
                result.map,
                result.time_limit,
                result.rules
            ))
        except Exception as e:
            await sent_message.edit(content=cm_submit.error + ":\n" + str_tab + str(e))
            return
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
    if content.startswith(cm_list.prefix + cm_challenge.command):
        tokens = content.split(' ')
        token_count = cm_list.token_count + cm_challenge.token_count
        error_message = content=cm_challenge.error + ":\n" + str_tab
        if len(tokens) != token_count + 6 and len(tokens) != token_count + 5:
            await sent_message.edit(error_message)
            return
            
        max_score_holers = 3
        if len(tokens) == token_count + 6:
            try:
                max_score_holers = int(tokens[token_count + 5])
            except:
                await sent_message.edit(error_message + cm_challenge.usage)
                return
        
        # Execute Command
        
        if not re.match(r'/geo challenge (add|remove)'):
            await sent_message.edit(error_message + "Please specify *add* or *remove* first")
            return
        add = tokens[token_count] == 'add'
        
        match_mode = re.match(r'.* mode=(point|speed|streak)( |$)')
        if not match_mode:
            await sent_message.edit(error_message + "Please specify a valid mode. E.g. *mode=point*")
            return
        mode = match_mode.group(1)
        
        
        
        
        match = re.match(r'/geo challenge (add|remove) (point|speed) map=[a-zA-Z0-9]+ (default|no-move|no-zoom|no-move-no-zoom|no-move-no-pan-no-zoom) (no-time-limit|[0-9]-([1-5]0)|[1-9]-([0-5]0)|10-00)($| )([1-9]$)', content)
        if not match:
            await sent_message.edit(error_message)
            return
        
        # TODO: Check Map exists
        
        # Execute Command
        
        mode = tokens[token_count + 1]
        map = tokens[token_count + 2]
        
        rules = Rules.DEFAULT
        if (tokens[token_count + 3] == 'no-move'):
            rules = Rules.NO_MOVE
        if (tokens[token_count + 3] == 'no-zoom'):
            rules = Rules.NO_ZOOM
        if (tokens[token_count + 3] == 'no-move-no-zoom'):
            rules = Rules.NO_MOVE_NO_ZOOM
        if (tokens[token_count + 3] == 'no-move-no-pan-no-zoom'):
            rules = Rules.NO_MOVE_NO_PAN_NO_ZOOM
        
        time_limit = Time(0, 0)
        
        
        challenge = Challenge(GeoguessrMap(device, tokens[token_count + 3]), Rules.NO_MOVE, time_limit=Time(2, 0))
        
        db.remove_table()
        
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