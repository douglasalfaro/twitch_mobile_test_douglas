# screens/home_screen.py
from selenium.webdriver.common.by import By  # kept for future tweaks if needed

class HomeScreen:
    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url: str):
        self.driver.get(base_url)

    def tap_search_icon(self):
        """Fastest & most reliable: go straight to the search route."""
        self.driver.get("https://m.twitch.tv/search")
