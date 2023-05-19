from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Load environment variables from .env file


class Driver():
    def __init__(self):
        self._chrome_driver_path='C:/Users/Morteza/Documents/Dev/chromedriver.exe'
        self._service=Service(executable_path=self._chrome_driver_path)
        self._driver=webdriver.Chrome(service=self._service)
        self._url=''
