import re
from typing import List
from bs4 import BeautifulSoup
from src.JSDevice import JSDevice
from src.GeoguessrPage import GeoguessrPage
from dataclasses import dataclass

@dataclass
class StreakItem:
    guess: str
    valid: bool = True
    correct_country: str = None

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, StreakItem):
            return False
        if self.guess != other.guess:
            return False
        if self.valid != other.valid:
            return False
        if self.correct_country != other.correct_country:
            return False
        return True

class GeoguessrStreak(GeoguessrPage):

    __RESULT_LIST = "streak-result-list"
    __RESULT_ITEM = "streak-result-list__item"

    __RESULT_ITEM_RIGHT = "streak-result-list__item--valid"
    __RESULT_ITEM_WRONG = "streak-result-list__item--invalid"

    __RESULT_COUNTRY_NAME = "streak-result-list__name-column"
    __RESULT_COUNTRY_SUBTEXT = "streak-result-list__sub-label"

    def __init__(self, device: JSDevice, code: str):
        super().__init__(device, code)
        self.__results = None

    @property
    def results(self) -> List[StreakItem]:
        """A list of each country guessed in the streak."""

        if self.__results is None:
            self.__results = []

            soup = BeautifulSoup(self.html, 'html.parser')
            countries = soup.find("div", {'class': self.__RESULT_LIST})
            for country in countries.find_all("li", {'class': self.__RESULT_ITEM }):
                name_div = country.find_next("div", {'class': self.__RESULT_COUNTRY_NAME })
                streak = StreakItem(name_div.text)
                if self.__RESULT_ITEM_WRONG in country['class']:
                    match = re.match(r'([\w\s]+)You guessed ([\w\s]+)\.', name_div.text)
                    streak.correct_country = match.group(1)
                    streak.guess = match.group(2)
                    streak.valid = False
                self.__results.append(streak)

        return self.__results

    @property
    def streak_count(self):
        return len([x for x in self.results if x.valid])
