from src import ChromeDevice, Database
import Command
import discord
import re

class CmSubmitCoop(Command):
    def matches_command(self, cm: str):
        return re.match(r'/geo submitcoop', cm)
    
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        await om.channel.send("not yet implemented soz")