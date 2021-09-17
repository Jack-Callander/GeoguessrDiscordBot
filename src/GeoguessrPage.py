from enum import Enum
from bs4 import BeautifulSoup
from src.JSDevice import JSDevice
from abc import ABC

class Rules(Enum):
    DEFAULT = 0
    NO_MOVE = 1
    NO_ZOOM = 2
    NO_MOVE_NO_ZOOM = 3
    NO_MOVE_NO_PAN_NO_ZOOM = 4
    
    def __lt__(self, other):
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

class GeoguessrPage(ABC):

    __URL_PREFIX = 'https://www.geoguessr.com/results/'
    __SIDEBAR_DIV_CLASS = 'default-sidebar-content'
    __GAME_BREAKDOWN = 'Game breakdown'

    def __init__(self, device: JSDevice, code: str):
        self.__device = device
        self.__code = code
        self.__html = None

    @property
    def code(self) -> str:
        return self.__code

    @property
    def html(self) -> str:
        if not self.__html:
            try:
                html = self.__device.fetch_html(self.__URL_PREFIX + self.__code)
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
