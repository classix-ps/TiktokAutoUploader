# This class will be in charge of uploading videos onto tiktok.
import os, time
from Bot import Bot
from Browser import Browser
from Cookies import Cookies
from selenium.common.exceptions import StaleElementReferenceException

from random import shuffle
from selenium.webdriver.common.by import By

class Upload:
    def __init__(self, user):
        self.bot = None
        self.lang = "en"
        self.account_url = f"https://www.tiktok.com/@discovergalaxies?lang={self.lang}"
        self.upload_url = f"https://www.tiktok.com/upload?lang={self.lang}"
        self.cookies = None
        self.newestVideoHref = None


    # This gets the hashtags from file and adds them to the website input
    def addCaptions(self, filename=None, hashtag_file=None):
        if not hashtag_file:
            caption_elem = self.webbot.getCaptionElem()
            caption = ""

            if filename:
                head, tail = os.path.split(filename)
                name = tail[:-4].replace('_', ' ')
                print(name)
                if len(name) > 48:
                    name = name[:47]
                caption += f"{name}. Image credit: ESA/Hubble, contains a sample of First Step by Hans Zimmer courtesy of WaterTowerMusic "
            hashtags = []
            with open("hashtags.txt", "r") as f:
                for line in f.readlines():
                    hashtags.append(line.replace("\n", ""))

            shuffle(hashtags)
            for hashtag in hashtags:
                toAppend = hashtag + ' '
                if len(caption) + len(toAppend) > 150:
                    break
                caption += toAppend

            caption_elem.send_keys(caption)


    def directUpload(self, filename, private=False, test=False):
        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)

        if self.newestVideoHref is None:
            self.bot.get(self.account_url)
            self.cookies = Cookies(self.bot)
            self.bot.refresh()
            self.newestVideoHref = self.webbot.getNewestVideoHref()
            print(self.newestVideoHref)
        else: # Additional check to avoid double uploads
            self.bot.refresh()
            newHref = self.webbot.getNewestVideoHref()
            if newHref != self.newestVideoHref:
                print("Double upload caught and avoided.")
                return true

        self.bot.get(self.upload_url)

        file_input_element = self.webbot.getVideoUploadInput()

        self.addCaptions(filename)

        abs_path = os.path.realpath(filename)
        file_input_element.send_keys(abs_path)

        print("Uploading...")
        self.webbot.uploadButtonClick()  # upload button
        print("Uploaded.")
        #self.webbot.waitUntilUploaded()
        print("Finished Uploading.")

        self.bot.get(self.account_url)

        newHref = self.webbot.getNewestVideoHref()
        print(newHref)
        return self.newestVideoHref != newHref
