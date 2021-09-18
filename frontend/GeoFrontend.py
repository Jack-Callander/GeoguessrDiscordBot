from frontend.Command import Command, CommandList
from src import Challenge, ChallengeType, ChromeDevice, Database, GeoguessrMap, GeoguessrResult, Player, Rules, Time
import re
import discord

class GeoFrontend:
    def __init__(self):
        # Commands
        self.tab = '    '
        self.cm_list = CommandList()
        self.cm_submit = Command('submit', 'Submit a record', 'submit <Game Brakdown URL>|<Game Code>', 'Error submitting')
        self.cm_submitcoop = Command('submitcoop', 'Submit a cooperative record', 'submitcoop <Game Brakdown URL>|<Game Code>', 'Error submitting')
        self.cm_renounce = Command('renounce', 'Renounce a record or cooperative record', 'renounce <Game Brakdown URL>|<Game Code>', 'Error renouncing')
        self.cm_challenge = Command('challenge', 'Add or Remove a Challenge on the highscores table', 'challenge add|remove type=point|speed|streak map=<MapID> default|no-move|no-zoom|no-move-no-zoom|no-move-no-pan-no-zoom no-time-limit|<MM>-<SS> [TopSpots=3]', 'Error adding or removing challenge')
        self.cm_highscores = Command('highscores', 'Show the highscores', 'highscores')
        self.cm_help = Command('help', 'Get Help on another command', 'help <Command name>', 'Failed to get help')
        
        self.cm_list.append(self.cm_submit)
        self.cm_list.append(self.cm_submitcoop)
        self.cm_list.append(self.cm_renounce)
        self.cm_list.append(self.cm_challenge)
        self.cm_list.append(self.cm_highscores)
        self.cm_list.append(self.cm_help)
    
    async def command_help(self, tokens, sm):
        if len(tokens) != 3:
            await sm.edit(content=self.cm_help.error + ":\n" + self.tab + self.cm_help.usage)
            return
        
        for cm in self.cm_list.list:
            if (cm.command == tokens[2]):
                out = "**Command Help**:\n"
                out += self.tab + "Name: *" + cm.command + "*\n"
                out += self.tab + "Desc: *" + cm.description + "*\n"
                out += self.tab + "Usage: *" + cm.usage + "*"
                
                await sm.edit(content=out)
                return
        
        await sm.edit(content="Unknown Command: *" + tokens[2] + "*")
    
    async def command_submit(self, tokens, sm, om, db, device):
        if len(tokens) != 3:
            await sm.edit(content=self.cm_submit.error + ":\n" + self.tab + self.cm_submit.usage)
            return
        
        code = tokens[2].split('/')[-1]
        result = GeoguessrResult(device, code)
        
        try:
            await sm.edit(content="**Submission Found!**\nScore: {0}\nDistance: {1}\nTime: {2}\nMap: {3}\nTime Limit: {4}\nRules: {5}".format(
                result.score,
                result.distance,
                result.time,
                result.map,
                result.time_limit,
                result.rules
            ))
        except Exception as e:
            await sm.edit(content=self.cm_submit.error + ":\n" + self.tab + str(e))
            return
        
        for rt in db.record_tables:
            if rt.challenge.is_applicable(result):
                rt.update(Player(om.author.id, om.author.name), result)
                db.save()
                await om.channel.send(content="**Submission Satisfies:** " + str(rt.challenge))
        
        return
    
    async def command_renounce(self, tokens, sm, om, db):
        if len(tokens) != 3:
            await sm.edit(content=self.cm_renounce.error + ":\n" + self.tab + self.cm_renounce.usage)
            return
        
        code = tokens[2].split('/')[-1]
        found_match = False
        for rt in db.record_tables:
            if rt.renounce(code):
                if not found_match:
                    found_match = True
                    await sm.edit(content="**Renouncing matches:**\n")
                await om.channel.send(content="Removing match: " + rt.challenge.get_print())
            
            
        if found_match:
            db.save()
            await om.channel.send(content="Done.")
        else:
            await sm.edit(content="No records match *" + code + "*")
        
        return
    
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
        
        # Help Command
        if command.startswith(self.cm_list.prefix + self.cm_help.command):
            await self.command_help(tokens, sent_message)
            return
        
        # Submit and SubmitCoop Command
        if command.startswith(self.cm_list.prefix + self.cm_submit.command) or command.startswith(self.cm_list.prefix + self.cm_submitcoop.command):
            await self.command_submit(tokens, sent_message, message, db, device)
            return
        
        # Renounce Command
        if command.startswith(self.cm_list.prefix + self.cm_renounce.command):
            await self.command_renounce(tokens, sent_message, message, db)
            return
        
        # Challenge Add
        if command.startswith(self.cm_list.prefix + self.cm_challenge.command):
            tokens = command.split(' ')
            token_count = self.cm_list.token_count + self.cm_challenge.token_count
            error_message = self.cm_challenge.error + ":\n" + self.tab
            if len(tokens) != token_count + 6 and len(tokens) != token_count + 5:
                await sent_message.edit(content=error_message + self.cm_challenge.usage)
                return
                
            max_score_holers = 3
            if len(tokens) == token_count + 6:
                try:
                    max_score_holers = int(tokens[token_count + 5])
                except:
                    await sent_message.edit(content=error_message + self.cm_challenge.usage)
                    return
            
            # Execute Command
            challenge = None
            
            # Add Remove
            print(command)
            match_add = re.search(r' (add|remove)( |$)', command)
            if not match_add:
                await sent_message.edit(content=error_message + "Please specify *add* or *remove*")
                return
            add = match_add.group(1) == "add"
            
            # Max Record Holders
            match_holders = re.match(r' mrh=([1-9])( |$)', command)
            holders = 3
            if match_holders:
                holders = int(match_holders.group(1))
            
            # Type
            match_type = re.search(r' type=(point|speed|streak)( |$)', command)
            if not match_type:
                await sent_message.edit(content=error_message + "Please specify a valid type. E.g. *type=point*")
                return
            type = ChallengeType.POINT
            if (match_type.group(1) == "speed"):
                type = ChallengeType.SPEED
            if (match_type.group(1) == "streak"):
                type = ChallengeType.STREAK
            
            
            if type == "streak":
                await sent_message.edit(content=error_message + "Not implemented soz")
                return
            
            # Map
            match_map = re.search(r' map=([a-zA-Z0-9]+)( |$)', command)
            if not match_map:
                await sent_message.edit(content=error_message + "Please specify a map code. E.g. *map=ABCdef123567*")
                return
            map = match_map.group(1)
            
            # Rules
            match_rules = re.search(r' (default|no-move|no-zoom|no-move-no-zoom|no-move-no-pan-no-zoom)( |$)', command)
            if not match_rules:
                await sent_message.edit(content=error_message + "Please specify a ruleset. E.g. *no-move*")
                return
            rules = Rules.DEFAULT
            if (match_rules.group(1) == 'no-move'):
                rules = Rules.NO_MOVE
            if (match_rules.group(1) == 'no-zoom'):
                rules = Rules.NO_ZOOM
            if (match_rules.group(1) == 'no-move-no-zoom'):
                rules = Rules.NO_MOVE_NO_ZOOM
            if (match_rules.group(1) == 'no-move-no-pan-no-zoom'):
                rules = Rules.NO_MOVE_NO_PAN_NO_ZOOM
            
            # Time Limit
            if type == ChallengeType.POINT:
                match_time = re.search(r' (no-time-limit|[0-9]-[1-5]0|[1-9]-[0-5]0|10-00)($| )', command)
                if not match_time:
                    await sent_message.edit(content=error_message + "Please specify a time limit. E.g. *no-time-limit* or *M-SS* where seconds are a multiple of 10 and *M* is 0 to 10")
                    return
                string_time = match_time.group(1)
                time = Time()
                if (string_time != "no-time-limit"):
                    time = Time(int(string_time.split('-')[0]), int(string_time.split('-')[1]))
                challenge = Challenge(GeoguessrMap(device, map), rules, type, time_limit=time)
            
            # Point
            if type == ChallengeType.SPEED:
                await sent_message.edit(content=error_message + "No Speedruns yet soz")
                return
            
            
            # Apply
            if add:
                if db.add_table(challenge, holders):
                    await sent_message.edit(content="**Challenge Added:**\n" + self.tab + "Map Code: " + str(challenge.map) + "\n" + self.tab + "Type: " + str(challenge.type) + "\n" + self.tab + "Time Limit: " + str(challenge.time_limit) + "\n" + self.tab + "Rules: " + str(challenge.rules) + "\n" + self.tab + "Max Record Holders: " + str(holders))
                else:
                    await sent_message.edit(content="*Challenge Specified already exists!*")
            else:
                if db.remove_table(challenge):
                    await sent_message.edit(content="*Challenge Removed*")
                else:
                    await sent_message.edit(content="*Specified Challenge not found*")
            
            return
            
        # Highscores
        if command.startswith(self.cm_list.prefix + self.cm_highscores.command):
            out_point = "**Point-Based:**\n"
            for rt in db.record_tables:
                out_point += self.tab + str(rt.challenge) + "\n"
                for record in rt.holders:
                    out_point += self.tab + self.tab + str(record.player.name) + str(record.result.score) + "\n"
            await sent_message.edit(content=out_point)
            
            return
        
        
        # Invalid Command
        await sent_message.edit(content="Unknown Command: *" + command + "*\n" + self.tab + "Type *" + self.cm_list.prefix.strip() + "* for a list of commands.")