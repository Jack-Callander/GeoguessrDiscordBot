from DiscordUser import Player
from GeoguessrResult import Time

class ScoreHolder:
    def __init__(self, player, score):
        pass

class TimeHolder:
    def __init__(self, player, time):
        pass


class Record:
    def __init__(self, cat, map, max_record_holders = 3):
        # TODO pass in categories that define this record, eg SpeedRun 24K on Diverse World
        #      maybe use enum for all the categories...
        self.holders = [None] * max_record_holders
    