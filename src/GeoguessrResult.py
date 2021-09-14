import re
from bs4 import BeautifulSoup
from src.JSDevice import JSDevice

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

class GeoguessrResult:

    __URL_PREFIX = 'https://www.geoguessr.com/results/'
    __OUTER_CLASS = 'results-highscore__guess-cell--total'
    __INNER_CLASS_SCORE = 'results-highscore__guess-cell-score'
    __INNER_CLASS_TIME = 'results-highscore__guess-cell-details'

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
        match = re.match(r'(\d+) m - (\d+) min, (\d+) sec', inner_div.text)
        return Time(int(match.group(2)), int(match.group(3))) if match else Time(0, 0)
    
    def __get_html(self):
        return self.__device.fetch_html(self.__URL_PREFIX + self.__code)
