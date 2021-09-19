from frontend import Command, CommandList
from src import ChromeDevice, Database
import discord
import re

class CmHelp(Command):
    def __init__(self, cm_list: CommandList, command: str, description: str, usage: str, error: str = "Command error") -> None:
        self.__cm_list = cm_list
        super().__init__(command, description, usage, error)

    def matches_command(self, cm: str):
        return re.match(r'/geo help( |$)', cm)
    
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        tokens = self._get_tokens(cm)
        if len(tokens) != 3:
            await sm.edit(content=self.error + ":\n" + self._tab + self.usage)
            return
        
        for cm in self.__cm_list.list:
            if (cm.command == tokens[2]):
                out = "**Command Help**:\n"
                out += self._tab + "Name: *" + cm.command + "*\n"
                out += self._tab + "Desc: *" + cm.description + "*\n"
                out += self._tab + "Usage: *" + cm.usage + "*"
                
                await sm.edit(content=out)
                return
        
        await sm.edit(content="Unknown Command: *" + tokens[2] + "*")