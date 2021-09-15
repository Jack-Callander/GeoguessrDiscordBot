import re
from typing import List
from bs4 import BeautifulSoup
from src.JSDevice import JSDevice
from dataclasses import dataclass
from enum import Enum

# https://www.geoguessr.com/results/eOpI74g7FUbUOtkt

class Time:
    def __init__(self, mins=0, secs=0):
        self.minutes = mins
        self.seconds = secs

    def __str__(self):
        return f'{self.minutes} min, {self.seconds} sec' if self.minutes > 0 else f'{self.seconds} sec'

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if not isinstance(other, Time):
            return False
        return self.minutes == other.minutes and self.seconds == other.seconds
    
    def __bool__(self):
        return self.minutes > 0 or self.seconds > 0

    @classmethod
    def zero(cls):
        return cls(mins=0, secs=0)

class Units(Enum):
    METRES = 'm'
    KILOMETRES = 'km'
    YARDS = 'yd'
    MILES = 'miles'

@dataclass
class Distance:
    value: float
    units: Units = Units.METRES

    def __str__(self):
        return f'{self.value} {self.units.value}'

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if not isinstance(other, Distance):
            return False
        return abs(self - other) < 1e-12
    
    def __abs__(self):
        return abs(self.value)

    def __add__(self, other):
        if not isinstance(other, Distance):
            raise TypeError
        return Distance(self.value + other.convert(self.units).value, units=self.units)

    def __sub__(self, other):
        if not isinstance(other, Distance):
            raise TypeError
        return Distance(self.value - other.convert(self.units).value, units=self.units)

    def convert(self, units: Units) -> 'Distance':
        """Converts the distance into the given units."""

        # 1 km = 1000 m
        # 1 yd = 0.9144 m
        # 1 mile = 1760 yd

        converted = self.value
        if self.units == Units.METRES:
            if units == Units.KILOMETRES:
                converted /= 1000
            elif units == Units.YARDS:
                converted /= 0.9144
            elif units == Units.MILES:
                converted /= 0.9144 * 1760
        elif self.units == Units.KILOMETRES:
            if units == Units.METRES:
                converted *= 1000
            elif units == Units.YARDS:
                converted *= 1000 / 0.9144
            elif units == Units.MILES:
                converted *= 1000 / (0.9144 * 1760)
        elif self.units == Units.YARDS:
            if units == Units.METRES:
                converted *= 0.9144
            elif units == Units.KILOMETRES:
                converted *= 0.9144 / 1000
            elif units == Units.MILES:
                converted /= 1760
        elif self.units == Units.MILES:
            if units == Units.METRES:
                converted *= 0.9144 * 1760
            elif units == Units.KILOMETRES:
                converted *= (0.9144 * 1760) / 1000
            elif units == Units.YARDS:
                converted *= 1760

        return Distance(converted, units=units)

@dataclass
class Round:
    points: int
    distance: Distance
    time: Time

    def __str__(self):
        return f'{self.points} pts, {self.distance} - {self.time}'

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if not isinstance(other, Round):
            return False
        if self.points != other.points:
            return False
        if self.distance != other.distance:
            return False
        if self.time != other.time:
            return False
        return True

class Rules(Enum):
    DEFAULT = 0
    NO_MOVE = 1
    NO_ZOOM = 2
    NO_MOVE_NO_ZOOM = 3
    NO_MOVE_NO_PAN_NO_ZOOM = 4

class GeoguessrResult:

    __URL_PREFIX = 'https://www.geoguessr.com/results/'

    __OUTER_CLASS_ROUND = 'results-highscore__guess-cell--round'
    __OUTER_CLASS_TOTAL = 'results-highscore__guess-cell--total'
    __OUTER_CLASS_INFO = 'result-info-card__content'

    __INNER_CLASS_SCORE = 'results-highscore__guess-cell-score'
    __INNER_CLASS_DETAILS = 'results-highscore__guess-cell-details'

    def __init__(self, device: JSDevice, code: str):
        self.__device = device
        self.__code = code

    def get_rounds(self) -> List[Round]:
        """Gets a list of details about each round in the Geoguessr run."""
        
        rounds = []
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        for round_div in soup.find_all("div", {'class': self.__OUTER_CLASS_ROUND}):
            score = self.__get_score(round_div)
            distance = self.__get_distance(round_div)
            time = self.__get_time(round_div)
            rounds.append(Round(score, distance, time))
        return rounds

    @property
    def score(self) -> int:
        """The total score for the Geoguessr run."""

        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_score(total_div)

    @property
    def distance(self) -> Distance:
        """The sum of all the distances in the Geoguessr run."""

        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_distance(total_div)
    
    @property
    def time(self) -> Time:
        """The total time taken to complete the Geoguessr run."""

        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_time(total_div)
    
    @property
    def map(self) -> str:
        """The map the Geoguessr run was in (by it's URL code on Geoguessr)."""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup.find_all("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[0] is left-hand info box at the top of the page, ie the map and map author
        inner_map_a = outer_div[0].find_next("a")
        map_code = inner_map_a["href"][6:]
        return map_code
        
    @property
    def time_limit(self) -> Time:
        """The time limit of the Geoguessr run (or `Time.zero()` if there is no time limit)."""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup.find_all("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[1] is right-hand info box at the top of the page, ie the time limit and rules
        inner_info_p = outer_div[1].find_next("p")
        return self.__str_to_Time(inner_info_p.text)
    
    @property
    def rules(self) -> Rules:
        """The movement rules that the Geoguessr run was played with."""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup.find_all("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[1] is right-hand info box at the top of the page, ie the time limit and rules
        inner_info_p = outer_div[1].find_next("p")
        no_move = re.match(r'.*No move', inner_info_p.text)
        no_pan = re.match(r'.*No pan', inner_info_p.text)
        no_zoom = re.match(r'.*No zoom', inner_info_p.text)
        r = Rules.DEFAULT
        if no_move and no_pan and no_zoom:
            r = Rules.NO_MOVE_NO_PAN_NO_ZOOM
        elif no_move and no_zoom:
            r = Rules.NO_MOVE_NO_ZOOM
        elif no_zoom:
            r = Rules.NO_ZOOM
        elif no_move:
            r = Rules.NO_MOVE
            
        return r
        
    def __str_to_Time(self, str) -> Time:
        match = re.search(r'(\d+) min.* (\d+) sec', str)
        if match:
            return Time(int(match.group(1)), int(match.group(2)))
        match = re.search(r'(\d+) min', str)
        if match:
            return Time(int(match.group(1)), 0)
        match = re.search(r'(\d+) sec', str)
        if match:
            return Time(0, int(match.group(1)))
        return Time()
    
    def __get_html(self) -> str:
        return self.__device.fetch_html(self.__URL_PREFIX + self.__code)

    def __get_score(self, div) -> int:
        score = div.find("div", {'class': self.__INNER_CLASS_SCORE})
        match = re.match(r'([\d,]+) pts', score.text)
        return int(match.group(1).replace(',', '')) if match else 0

    def __get_distance(self, div) -> Distance:
        inner_div = div.find("div", {'class': self.__INNER_CLASS_DETAILS})
        match = re.match(r'(\d+) (m|km|yd|miles)', inner_div.text)
        units = next(x for x in Units if x.value == match.group(2))
        return Distance(int(match.group(1)), units=units)

    def __get_time(self, div) -> Time:
        inner_div = div.find("div", {'class': self.__INNER_CLASS_DETAILS})
        match = re.match(r'.* - (?:(\d+) min, )?(\d+) sec', inner_div.text)
        mins = match.group(1)
        secs = match.group(2)
        return Time(int(mins), int(secs)) if mins else Time(0, int(secs))
