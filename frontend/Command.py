class Command():
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
    
    def get_print(self, tab) -> str:
        out = "**Command List:**\n"
        for cm in self.list:
            out += tab + self.prefix + cm.description + "\n"
        return out
    
    @property
    def token_count(self) -> int:
        return len(self.prefix.strip().split(' '))