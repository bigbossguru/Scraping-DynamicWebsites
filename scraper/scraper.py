from typing import Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Scraper:
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=self.options
        )

    def get_static_page_content(self, url: str) -> str:
        return requests.get(url).text

    def get_dynamic_page_content(self, url: str) -> str:
        self.driver.get(url)
        return self.driver.page_source

    def searcher(self, page_content: Optional[str]) -> BeautifulSoup:
        page_content = page_content or self.driver.page_source
        soup = BeautifulSoup(page_content, "lxml")
        return soup
