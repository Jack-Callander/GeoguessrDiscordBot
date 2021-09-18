import re
from typing import List
from bs4 import BeautifulSoup
from src.GeoguessrActivity import GeoguessrActivity, Time
from src.JSDevice import JSDevice
from dataclasses import dataclass
from enum import Enum

# https://www.geoguessr.com/results/eOpI74g7FUbUOtkt

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
        if not isinstance(other, Round):
            return False
        if self.points != other.points:
            return False
        if self.distance != other.distance:
            return False
        if self.time != other.time:
            return False
        return True

class GeoguessrResult(GeoguessrActivity):

    __OUTER_CLASS_ROUND = 'results-highscore__guess-cell--round'
    __OUTER_CLASS_TOTAL = 'results-highscore__guess-cell--total'

    __INNER_CLASS_SCORE = 'results-highscore__guess-cell-score'
    __INNER_CLASS_DETAILS = 'results-highscore__guess-cell-details'

    def __init__(self, device: JSDevice, code: str, db):
        super().__init__(device, code, db)

    def get_rounds(self) -> List[Round]:
        """Gets a list of details about each round in the Geoguessr run."""
        
        rounds = []
        soup = BeautifulSoup(self.html, 'html.parser')
        for round_div in soup.find_all("div", {'class': self.__OUTER_CLASS_ROUND}):
            score = self.__get_score(round_div)
            distance = self.__get_distance(round_div)
            time = self.__get_time(round_div)
            rounds.append(Round(score, distance, time))
        return rounds

    @property
    def score(self) -> int:
        """The total score for the Geoguessr run."""

        soup = BeautifulSoup(self.html, 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_score(total_div)

    @property
    def distance(self) -> Distance:
        """The sum of all the distances in the Geoguessr run."""

        soup = BeautifulSoup(self.html, 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_distance(total_div)
    
    @property
    def time(self) -> Time:
        """The total time taken to complete the Geoguessr run."""

        soup = BeautifulSoup(self.html, 'html.parser')
        total_div = soup.find("div", {'class': self.__OUTER_CLASS_TOTAL})
        return self.__get_time(total_div)

    def __get_score(self, div) -> int:
        score = div.find("div", {'class': self.__INNER_CLASS_SCORE})
        match = re.match(r'([\d,]+) pts', score.text)
        return int(match.group(1).replace(',', '')) if match else 0

    def __get_distance(self, div) -> Distance:
        inner_div = div.find("div", {'class': self.__INNER_CLASS_DETAILS})
        match = re.match(r'([\d,.]+) (m|km|yd|miles)', inner_div.text)
        units = next(x for x in Units if x.value == match.group(2))
        return Distance(float(match.group(1).replace(',', '')), units=units)

    def __get_time(self, div) -> Time:
        inner_div = div.find("div", {'class': self.__INNER_CLASS_DETAILS})
        return Time.from_str(inner_div.text[inner_div.text.index('-')+1:])
