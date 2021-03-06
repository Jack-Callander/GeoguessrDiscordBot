from typing import List
from src.Challenge import Challenge
from src.DiscordUser import Player
from src.GeoguessrResult import GeoguessrResult
from abc import ABC, abstractmethod
from copy import copy, deepcopy

class Record(ABC):

    def __init__(self, player: Player, result: GeoguessrResult):
        self.__player = player
        self.__result = result

    @property
    def player(self) -> Player:
        return self.__player
    
    @property
    def result(self) -> GeoguessrResult:
        return self.__result

    @abstractmethod
    def get_print(self) -> str:
        pass

    @abstractmethod
    def __lt__(self, other):
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class ScoreHolder(Record):

    def __init__(self, player: Player, result: GeoguessrResult):
        super().__init__(player, result)
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, ScoreHolder):
            raise TypeError
        return self.result.score < other.result.score
    
    def __str__(self) -> str:
        s = "Player: " + str(self.player) + ", "
        s += "Score: " + str(self.result.score)
        return s
        
    def get_print(self) -> str:
        out = "**" + str(self.player) + f'** - *[{self.result.score:,}]({self.result.link})*'
        return out

class TimeHolder(Record):

    def __init__(self, player: Player, result: GeoguessrResult):
        super().__init__(player, result)
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, TimeHolder):
            raise TypeError
        return self.result.time > other.result.time
        
    def __str__(self) -> str:
        s = "Player: " + str(self.player) + ", "
        s += "Time: " + str(self.result.time)
        return s
    
    def get_print(self) -> str:
        out = "**" + str(self.player) + "** - *" + str(self.result.time) + "*"
        return out

class RecordTable:
    
    def __init__(self, challenge: Challenge, max_record_holders: int = 3):
        self.__challenge = challenge
        self.__max_record_holders = max_record_holders
        self.__holders = []
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, RecordTable):
            return False
        return self.__challenge == other.__challenge
        
    def __lt__(self, other) -> bool:
        if self is other:
            return False
        if not isinstance(other, RecordTable):
            raise TypeError
        return self.challenge < other.challenge
    
    @property
    def challenge(self) -> Challenge:
        return copy(self.__challenge)
    
    @property
    def max_record_holders(self) -> int:
        return self.__max_record_holders
    
    @property
    def holders(self) -> List[Record]:
        return sorted(self.__holders.copy(), reverse=True)

    def update(self, player: Player, result: GeoguessrResult) -> bool:
        holder = None
        if self.challenge.point_target > 0:
            holder = TimeHolder(player, result)
        else:
            holder = ScoreHolder(player, result)
        
        if not self.challenge.is_applicable(result):
            return False
        
        self.__holders = [x for x in self.holders if x.player != player]
        self.__holders.append(holder)
        
        return True
    
    def renounce(self, code: str, user_id) -> bool:
        prev_length = len(self.holders)
        self.__holders = [x for x in self.holders if x.result.code != code or x.player.id != user_id]
        return prev_length != len(self.holders)
    
    def get_print(self, tab: str) -> str:
        out = tab + str(self.challenge.rules) + "\n"
        out += self.get_print_desc(tab)
        return out
    
    def get_print_desc(self, tab: str) -> str:
        out = ""
        
        holder_count = min(self.max_record_holders, len(self.holders))
        if holder_count == 0:
            out += tab + "\u2800" * 2 + '*There have been no attempts at this challenge.*\n'
            return out
        
        for i in range(0, holder_count):
            preface = "\u2800" * 2
            if i == 0:
                preface = ":first_place:"
            if i == 1:
                preface = ":second_place:"
            if i == 2:
                preface = ":third_place:"
            
            out += tab + "\u2800" * 2 + preface + self.holders[i].get_print() + "\n"
        
        return out