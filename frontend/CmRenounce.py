from src import ChromeDevice, Database
from frontend import Command
import discord
import re

class CmRenounce(Command):
    def matches_command(self, cm: str):
        return re.match(r'/geo renounce( |$)', cm) 
    
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        tokens = self._get_tokens(cm)
        if len(tokens) != 3:
            await sm.edit(content=self.error + ":\n" + self._tab + self.usage)
            return
        
        code = tokens[2].split('/')[-1]
        found_match = False
        for rt in db.record_tables:
            if rt.renounce(code, om.author.id):
                if not found_match:
                    found_match = True
                    await sm.edit(content="**Renouncing matches:**\n")
                await om.channel.send(content="Removing match: " + rt.challenge.get_print())
            
        if found_match:
            db.save()
            await om.channel.send(content="Done.")
        else:
            await sm.edit(content="No records match *" + code + "* under *" + om.author.name + "*")