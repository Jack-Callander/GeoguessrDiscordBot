from dataclasses import dataclass
from enum import Enum
from src.GeoguessrActivity import Rules, Time
from src.GeoguessrResult import GeoguessrResult
from src.GeoguessrMap import GeoguessrMap

class ChallengeType(Enum):
    POINT = 0
    STREAK = 1
    SPEED = 2
    
    def __lt__(self, other) -> bool:
        if self is other:
            return False
        if not isinstance(other, ChallengeType):
            raise TypeError
        return self.value < other.value
    
    def __str__(self) -> str:
        if self.value == ChallengeType.POINT.value:
            return "Point-Based"
        if self.value == ChallengeType.STREAK.value:
            return "Streak"
        if self.value == ChallengeType.SPEED.value:
            return "Speedrun"

@dataclass
class Challenge:
    map: GeoguessrMap
    rules: Rules
    type: ChallengeType = ChallengeType.POINT
    time_limit: Time = None
    point_target: int = 0
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Challenge):
            return False
        if self.map != other.map:
            return False
        if self.rules != other.rules:
            return False
        if self.time_limit != other.time_limit:
            return False
        if self.point_target != other.point_target:
            return False
        return True
        
    def __lt__(self, other) -> bool:
        if self is other:
            return False
        if not isinstance(other, Challenge):
            raise TypeError
        if self.type == other.type:
            if self.map == other.map:
                if self.rules == other.rules:
                    if self.time_limit != None:
                        return self.time_limit < other.time_limit
                    else:
                        return self.point_target < other.point_target
                else:
                    return self.rules < other.rules
            else:
                return self.map < other.map
        else:
            return self.type < other.type

    def __str__(self) -> str:
        return str(self.type) + ", Map=" + str(self.map) + ", " + str(self.rules) + ", " + str(self.time_limit) + ", " + str(self.point_target)

    def is_applicable(self, result: GeoguessrResult) -> bool:
        if self.map != result.map:
            return False
        if self.rules > result.rules:
            return False
        if self.rules == Rules.NO_MOVE and result.rules == Rules.NO_ZOOM:
            return False
        if self.rules == Rules.NO_ZOOM and result.rules == Rules.NO_MOVE:
            return False
        if self.time_limit and self.time_limit < max(x.time for x in result.get_rounds()):
            return False
        if self.point_target > 0 and self.point_target > result.score:
            return False
        return True
