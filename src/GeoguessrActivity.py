import re
from abc import ABC
from enum import Enum
from bs4 import BeautifulSoup
from src.GeoguessrMap import GeoguessrMap
from src.JSDevice import JSDevice

class Time:

    def __init__(self, mins=0, secs=0):
        self.minutes = mins
        self.seconds = secs

    def __str__(self):
        return f'{self.minutes} min, {self.seconds} sec' if self.minutes > 0 else f'{self.seconds} sec'

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Time):
            return False
        return self.minutes == other.minutes and self.seconds == other.seconds
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, Time):
            return False
        if self.minutes > other.minutes:
            return False
        if self.minutes == other.minutes and self.seconds >= other.seconds:
            return False
        return True

    def __bool__(self):
        return self.minutes > 0 or self.seconds > 0

    @classmethod
    def zero(cls):
        return cls(mins=0, secs=0)

    @classmethod
    def from_str(cls, text: str) -> 'Time':
        match = re.match(r'(?:(\d+) (?:hr|hours?)(?:,| and)?(?:\s|$))?(?:(\d+) min\w*(?:,| and)?(?:\s|$))?(?:(\d+) sec\w*$)?', text.strip())

        hours_match = match.group(1)
        mins_match = match.group(2)
        secs_match = match.group(3)

        hours = int(hours_match) if hours_match else 0
        mins = int(mins_match) if mins_match else 0
        secs = int(secs_match) if secs_match else 0

        return cls(hours * 60 + mins, secs)

class Rules(Enum):
    DEFAULT = 0
    NO_MOVE = 1
    NO_ZOOM = 2
    NO_MOVE_NO_ZOOM = 3
    NO_MOVE_NO_PAN_NO_ZOOM = 4
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, Rules):
            return TypeError
        return self.value < other.value
    
    def __str__(self) -> str:
        if self.value == Rules.DEFAULT.value:
            return "Default"
        elif self.value == Rules.NO_MOVE.value:
            return "No Move"
        elif self.value == Rules.NO_ZOOM.value:
            return "No Zoom"
        elif self.value == Rules.NO_MOVE_NO_ZOOM.value:
            return "No Move, No Zoom"
        elif self.value == Rules.NO_MOVE_NO_PAN_NO_ZOOM.value:
            return "No Move, No Pan, No Zoom"
        return "Unknown"

class GeoguessrActivity(ABC):

    __URL_PREFIX = 'https://www.geoguessr.com/results/'
    __SIDEBAR_DIV_CLASS = 'default-sidebar-content'
    __GAME_BREAKDOWN = 'Game breakdown'
    __OUTER_CLASS_INFO = 'result-info-card__content'

    def __init__(self, device: JSDevice, code: str):
        self.__device = device
        self.__code = code
        self.__html = None

    @property
    def code(self) -> str:
        return self.__code

    @property
    def device(self) -> JSDevice:
        return self.__device    

    @property
    def html(self) -> str:
        if not self.__html:
            try:
                html = self.device.fetch_html(self.__URL_PREFIX + self.code)
            except:
                raise Exception("Failed to connect to Link provided.")
            else:
                soup = BeautifulSoup(html, 'html.parser')
                h1s = soup.find_all("h1")
                sidebar_div = soup.find("div", {'class': self.__SIDEBAR_DIV_CLASS})
                
                has_game_breakdown = False
                for h1 in h1s:
                    if (h1.text == self.__GAME_BREAKDOWN):
                        has_game_breakdown = True
                        
                if not sidebar_div or not has_game_breakdown:
                    raise Exception("Failed to load Geoguessr site.")
                self.__html = html
        return self.__html

    @property
    def map(self) -> str:
        """The map the Geoguessr run was in."""
    
        soup = BeautifulSoup(self.html, 'html.parser')
        outer_div = soup.find_all("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[0] is left-hand info box at the top of the page, ie the map and map author
        inner_map_a = outer_div[0].find_next("a")
        # TODO: Get map name and author.
        map_code = inner_map_a["href"][6:] if inner_map_a else None
        return GeoguessrMap(self.device, map_code)

    @property
    def time_limit(self) -> Time:
        """The time limit of the Geoguessr activity (or `Time.zero()` if there is no time limit)."""
    
        soup = BeautifulSoup(self.html, 'html.parser')
        outer_div = soup.find_all("div", {'class': self.__OUTER_CLASS_INFO}, limit=2)
        # outer_div[1] is right-hand info box at the top of the page, ie the time limit and rules
        inner_info_p = outer_div[1].find_next("p")
        if "No time limit" in inner_info_p.text:
            return Time.zero()
        match = re.match(r'Max ([\w\s]+) per round', inner_info_p.text)
        return Time.from_str(match.group(1))
    
    @property
    def rules(self) -> Rules:
        """The movement rules that the Geoguessr activity was played with."""
    
        soup = BeautifulSoup(self.html, 'html.parser')
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