from abc import ABC, abstractmethod
from src import Database
from src import ChromeDevice
import discord


class Command(ABC):
    def __init__(self, command: str, description: str, usage: str, error: str = "Command error"):
        self.__command = command
        self.__description = description
        self.__usage = usage
        self.__error = error
        
        self._tab = '    '
    
    @property
    def command(self) -> str:
        return self.__command
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def usage(self) -> str:
        return self.__usage
    
    @property
    def error(self) -> str:
        return self.__error
    
    @abstractmethod
    def matches_command(self, cm: str):
        pass
    
    @abstractmethod
    async def run_command(self, cm: str, om: discord.Message, sm: discord.Message, device: ChromeDevice, db: Database):
        pass
    
    def _get_tokens(self, cm: str):
        return cm.split(' ')

class CommandList:
    def __init__(self):
        self.list = []
        self.prefix = "/geo "
    
    def append(self, cm: Command):
        self.list.append(cm)
    
    def get_print(self, tab) -> str:
        out = "**Command List:**\n"
        for cm in self.list:
            out += tab + self.prefix + cm.command + " - " + cm.description + "\n"
        return out
    
    @property
    def token_count(self) -> int:
        return len(self.prefix.strip().split(' '))