import undetected_chromedriver.v2 as uc
from fake_useragent import UserAgent, FakeUserAgentError
# import os
# https://github.com/ultrafunkamsterdam/undetected-chromedriver


# Class used to create undetectable selenium bot
class Browser:
    def __init__(self):
        try:
            ua = UserAgent()
            self.user_agent = ua.random
        except FakeUserAgentError:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = uc.ChromeOptions()
        # options.add_argument("--user-agent=" + self.user_agent)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        self.bot = uc.Chrome(options=options)
        self.bot.delete_all_cookies()

    def getBot(self):
        return self.bot

