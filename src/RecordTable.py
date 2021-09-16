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
    def __lt__(self, other):
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

class TimeHolder(Record):

    def __init__(self, player: Player, result: GeoguessrResult):
        super().__init__(player, result)
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, TimeHolder):
            raise TypeError
        return self.result.time > other.result.time

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
