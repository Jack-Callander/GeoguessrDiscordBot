from dataclasses import dataclass
from src.GeoguessrMap import GeoguessrMap
from src.GeoguessrResult import GeoguessrResult, Rules, Time

@dataclass
class Challenge:
    map: GeoguessrMap
    rules: Rules
    time_limit: Time = None
    point_target: int = 0

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
    