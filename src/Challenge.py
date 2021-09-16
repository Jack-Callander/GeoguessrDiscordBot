from dataclasses import dataclass
from src.GeoguessrResult import GeoguessrResult, Rules, Time
from src.GeoguessrMap import GeoguessrMap

@dataclass
class Challenge:
    map: GeoguessrMap
    rules: Rules
    time_limit: Time = None
    point_target: int = 0
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Challenge):
            return False
        return self.map == other.map and self.rules == other.rules and self.time_limit == other.time_limit and self.point_target == other.point_target

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
