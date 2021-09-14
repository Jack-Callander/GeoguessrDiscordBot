import re
from typing import Reversible
from bs4 import BeautifulSoup
from src.JSDevice import JSDevice
from enum import Enum

class Time:

    def __init__(self):
        self.__init__(0, 0)

    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        return f'{self.minutes} min, {self.seconds} sec'

    def __eq__(self, other):
        if self is None:
            return False
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.minutes == other.minutes and self.seconds == other.seconds

class Rules(Enum):
    default = 0
    no_move = 1
    no_zoom = 2
    no_move_no_zoom = 3
    no_move_no_pan_no_zoom = 4

class GeoguessrResult:

    __URL_PREFIX = 'https://www.geoguessr.com/results/'
    __OUTER_CLASS = 'results-highscore__guess-cell--total'
    __INNER_CLASS_SCORE = 'results-highscore__guess-cell-score'
    __INNER_CLASS_TIME = 'results-highscore__guess-cell-details'
    __OUTER_CLASS_INFO = 'result-info-card__content'

    def __init__(self, device: JSDevice, code: str):
        self.__device = device
        self.__code = code
    
    @property
    def score(self) -> int:
        """The total score for the Geoguessr run."""

        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup.find("div", {'class': self.__OUTER_CLASS})
        inner_div = outer_div.find("div", {'class': self.__INNER_CLASS_SCORE})
        match = re.match(r'([\d,]+) pts', inner_div.text)
        return int(match.group(1).replace(',', '')) if match else 0

    @property
    def time(self) -> Time:
        """The total time taken to complete the Geoguessr run."""

        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup.find("div", {'class': self.__OUTER_CLASS})
        inner_div = outer_div.find("div", {'class': self.__INNER_CLASS_TIME})
        match = re.match(r'.* - (\d+) min, (\d+) sec', inner_div.text)
        t = Time(0, 0)
        if match:
            # Minutes and Seconds
            t = Time(int(match.group(1)), int(match.group(2)))
        else:
            # Only Seconds
            match = re.match(r'.* - (\d+) sec', inner_div.text)
            t = Time(0, int(match.group(1)))
        return t
    
    @property
    def map(self) -> str:
        """The map the Geoguessr run was in (by it's URL code on Geoguessr)"""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[0] is left-hand info box at the top of the page, ie the map and map author
        inner_map_a = outer_div[0].find("a")
        map_code = inner_map_a["href"][6:]
        return map_code
        
    @property
    def time_limit(self) -> Time:
        """The map the Geoguessr run was in (by it's URL code on Geoguessr)"""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[1] is right-hand info box at the top of the page, ie the time limit and rules
        inner_info_p = outer_div[1].find("p")
        match = re.match(r'Max (\d+) minutes and (\d+) sec', inner_info_p.text)
        t = Time(0, 0)
        if match:
            # Minutes and Seconds
            t = Time(int(match.group(1)), int(match.group(2)))
        else:
            # Only Seconds
            match = re.match(r'Max (\d+) sec', inner_info_p.text)
            if match:
                t = Time(0, int(match.group(1)))
            else:
                # No Limit
                t = Time(0, 0)
        return t
    
    @property
    def rules(self) -> Rules:
        """The map the Geoguessr run was in (by it's URL code on Geoguessr)"""
    
        soup = BeautifulSoup(self.__get_html(), 'html.parser')
        outer_div = soup("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[1] is right-hand info box at the top of the page, ie the time limit and rules
        inner_info_p = outer_div[1].find("p")
        no_move = re.match(r'.*No move', inner_info_p.text)
        no_pan = re.match(r'.*No pan', inner_info_p.text)
        no_zoom = re.match(r'.*No zoom', inner_info_p.text)
        r = Rules.default
        if (no_move and no_pan and no_zoom):
            r = Rules.no_move_no_pan_no_zoom
        elif (no_move and no_zoom):
            r = Rules.no_move_no_zoom
        elif (no_zoom):
            r = Rules.no_zoom
        elif (no_move):
            r = Rules.no_move
            
        return r
    
    def __get_html(self):
        return self.__device.fetch_html(self.__URL_PREFIX + self.__code)
