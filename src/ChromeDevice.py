from selenium import webdriver
from src.JSDevice import JSDevice

class ChromeDevice(JSDevice):

    cache = {}

    def __init__(self, path: str):
        self.__path = path

    def fetch_html(self, url: str) -> str:
        if url in self.cache:
            return self.cache[url]
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        self.cache[url] = html
        return html
