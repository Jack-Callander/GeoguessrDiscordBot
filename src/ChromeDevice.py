from selenium import webdriver
from src.JSDevice import JSDevice
import os.path

class ChromeDevice(JSDevice):

    cache = {}

    def __init__(self, path: str):
        self.__path = path

    def fetch_html(self, url: str) -> str:
        if url in self.cache:
            return self.cache[url]
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = None

        if (os.path.isfile(".usingreplit")):
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=chrome_options)
        else:
            driver = webdriver.Chrome("D:/chromedriver.exe", options=chrome_options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        self.cache[url] = html
        return html
