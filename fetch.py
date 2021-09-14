import re
from bs4 import BeautifulSoup
from selenium import webdriver

URL_PREFIX = 'https://www.geoguessr.com/results/'
TEST_RUN = "eOpI74g7FUbUOtkt"

OUTER_CLASS = 'results-highscore__guess-cell--total'
INNER_CLASS_SCORE = 'results-highscore__guess-cell-score'
INNER_CLASS_TIME = 'results-highscore__guess-cell-details'

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
        if not isinstance(self, Time):
            return False
        return self.minutes == other.minutes and self.seconds == other.seconds

HTML_CACHE = {}
def fetch_html(url: str) -> str:
    """Fetches the HTML data from the given webpage."""

    if url in HTML_CACHE:
        return HTML_CACHE[url]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)
    driver.get(url)
    html = driver.execute_script("return document.body.innerHTML;")
    driver.quit()

    HTML_CACHE[url] = html
    return html

def get_score(code: str) -> int:
    """Gets the total score for the given Geoguessr run."""

    html = fetch_html(URL_PREFIX + code)
    soup = BeautifulSoup(html, 'html.parser')
    outer_div = soup.find("div", {'class': OUTER_CLASS})
    inner_div = outer_div.find("div", {'class': INNER_CLASS_SCORE})
    match = re.match(r'([\d,]+) pts', inner_div.text)
    return int(match.group(1).replace(',', '')) if match else 0

def get_time(code: str) -> Time:
    """Gets the time taken for the given Geoguessr run."""

    html = fetch_html(URL_PREFIX + code)
    soup = BeautifulSoup(html, 'html.parser')
    outer_div = soup.find("div", {'class': OUTER_CLASS})
    inner_div = outer_div.find("div", {'class': INNER_CLASS_TIME})
    match = re.match(r'(\d+) m - (\d+) min, (\d+) sec', inner_div.text)
    return Time(int(match.group(2)), int(match.group(3))) if match else Time(0, 0)

assert get_score(TEST_RUN) == 24492
assert get_time(TEST_RUN) == Time(4, 7)
