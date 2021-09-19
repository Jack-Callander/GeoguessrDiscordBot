from frontend import Command, CommandList, CmSubmit, CmSubmitCoop, CmRenounce, CmChallenge, CmHighscores, CmHelp
from src import Challenge, ChallengeType, ChromeDevice, Database, GeoguessrMap, GeoguessrResult, Player, Rules, Time
import re
import discord

class GeoFrontend:
    def __init__(self):
        # Commands
        self.tab = '    '
        self.cm_list = CommandList()
        cm_submit = CmSubmit('submit', 'Submit a record', 'submit <Game Brakdown URL>|<Game Code>', 'Error submitting')
        cm_submitcoop = CmSubmitCoop('submitcoop', 'Submit a cooperative record', 'submitcoop <Game Brakdown URL>|<Game Code>', 'Error submitting')
        cm_renounce = CmRenounce('renounce', 'Renounce a record or cooperative record', 'renounce <Game Brakdown URL>|<Game Code>', 'Error renouncing')
        cm_challenge = CmChallenge('challenge', 'Add or Remove a Challenge on the highscores table', 'challenge add|remove type=point|speed|streak map=<MapID> default|no-move|no-zoom|no-move-no-zoom|no-move-no-pan-no-zoom no-time-limit|<MM>-<SS> [TopSpots=3]', 'Error adding or removing challenge')
        cm_highscores = CmHighscores('highscores', 'Show the highscores', 'highscores')
        cm_help = CmHelp(self.cm_list, 'help', 'Get Help on another command', 'help <Command name>', 'Failed to get help')
        
        self.cm_list.append(cm_submit)
        self.cm_list.append(cm_submitcoop)
        self.cm_list.append(cm_renounce)
        self.cm_list.append(cm_challenge)
        self.cm_list.append(cm_highscores)
        self.cm_list.append(cm_help)
    
    async def on_message(self, message: str, client: discord.Client, device: ChromeDevice, db: Database):
    
        # New Received Message Content
        command = re.sub(r' +', ' ', message.content.strip())
        tokens = command.split(' ')
        
        # Command List (produced by only typing the command prefix)
        if command == self.cm_list.prefix.strip():
            await message.channel.send(self.cm_list.get_print(self.tab))
            return
        
        # All Commands
        if not command.startswith(self.cm_list.prefix.strip()):
            return
        
        sent_message = await message.channel.send("*Processing request...*")
        print("Processing: " + command)
        
        # Run Command if valid
        for cm in self.cm_list:
            if cm.matches_command(command):
                cm.run_command(cm, message, sent_message, device, db)
                return
        
        # Invalid Command
        await sent_message.edit(content="Unknown Command: *" + command + "*\n" + self.tab + "Type *" + self.cm_list.prefix.strip() + "* for a list of commands.")