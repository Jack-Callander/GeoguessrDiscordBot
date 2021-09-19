from src import ChromeDevice, Database, GeoguessrResult, Player
from frontend import Command
import discord
import re

class CmSubmit(Command):
    def matches_command(self, cm: str):
        return re.match(r'/geo submit( |$)', cm)
    
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        tokens = self._get_tokens(cm)
        if len(tokens) != 3:
            await sm.edit(content=self.error + ":\n" + self._tab + self.usage)
            return
        
        code = tokens[2].split('/')[-1]
        result = GeoguessrResult(device, code, db)
        
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
            await sm.edit(content=self.error + ":\n" + self._tab + str(e))
            return
        
        for rt in db.record_tables:
            if rt.challenge.is_applicable(result):
                rt.update(Player(om.author.id, om.author.name), result)
                db.save()
                await om.channel.send(content="**Submission Satisfies:** " + rt.challenge.get_print())
        
        return