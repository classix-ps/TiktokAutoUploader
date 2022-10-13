# This class will be in charge of uploading videos onto tiktok.
import os, time
from Bot import Bot
from Browser import Browser
from Cookies import Cookies
from Video import Video
from selenium.common.exceptions import StaleElementReferenceException

from random import shuffle
from selenium.webdriver.common.by import By

class Upload:
    def __init__(self, account, cookie):
        self.bot = None
        self.lang = "en"
        self.account_url = f"https://www.tiktok.com/@{account}?lang={self.lang}"
        self.upload_url = f"https://www.tiktok.com/upload?lang={self.lang}"
        self.cookie = cookie
        self.cookies = None
        self.newestVideoHref = None
        self.video = None
        self.videoSaveDir = "VideosDirPath"

    # This gets the hashtags from file and adds them to the website input
    def addCaptions(self, filename=None, hashtag_file=None):
        caption_elem = self.webbot.getCaptionElem()
        caption = ""

        if filename:
            head, tail = os.path.split(filename)
            name = tail[:-4].replace('_', ' ')
            print(name)
            if len(name) > 48:
                name = name[:47]
            caption += f"{name}. Image credit: ESA/Hubble, contains a sample of First Step by Hans Zimmer courtesy of WaterTowerMusic "
        
        if hashtag_file:
            hashtags = []
            with open(hashtag_file, "r") as f:
                for line in f.readlines():
                    hashtags.append(line.replace("\n", ""))

            shuffle(hashtags)
            for hashtag in hashtags:
                toAppend = hashtag + ' '
                if len(caption) + len(toAppend) > 150:
                    break
                caption += toAppend

        caption_elem.send_keys(caption)


    def directUpload(self, filename, hashtag_file):
        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)

        if self.newestVideoHref is None:
            self.bot.get(self.account_url)
            self.cookies = Cookies(self.bot, self.cookie)
            self.bot.refresh()
            self.newestVideoHref = self.webbot.getNewestVideoHref()
            print(self.newestVideoHref)
        else: # Additional check to avoid double uploads
            self.bot.refresh()
            newHref = self.webbot.getNewestVideoHref()
            if newHref != self.newestVideoHref:
                print("Double upload caught and avoided.")
                return True

        self.bot.get(self.upload_url)

        file_input_element = self.webbot.getVideoUploadInput()

        self.addCaptions(filename, hashtag_file)

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

    def uploadVideo(self, video_dir, videoText, startTime, endTime, hashtag_file):
        video_dir = self.downloadIfYoutubeURL(video_dir)
        if not video_dir:
            return false

        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)

        if self.newestVideoHref is None:
            self.bot.get(self.account_url)
            self.cookies = Cookies(self.bot, self.cookie)
            self.bot.refresh()
            self.newestVideoHref = self.webbot.getNewestVideoHref()
            print(self.newestVideoHref)
        else: # Additional check to avoid double uploads
            self.bot.refresh()
            newHref = self.webbot.getNewestVideoHref()
            if newHref != self.newestVideoHref:
                print("Double upload caught and avoided.")
                return True

        self.bot.get(self.upload_url)

        file_input_element = self.webbot.getVideoUploadInput()

        self.addCaptions()

        if self.video is None:
            self.video = Video(video_dir, videoText, self.videoSaveDir)
            print(f"startTime: {startTime}, endTime: {endTime}")
            self.video.customCrop(startTime, endTime)

            self.video.createVideo()  # Link to video class method
            while not os.path.exists(self.video.dir):  # Wait for path to exist
                pass

        abs_path = os.path.join(os.getcwd(), self.video.dir)
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

    def downloadIfYoutubeURL(self, video_dir) -> str:
        """
        Function will determine whether given video directory is a youtube link, returning the downloaded video path
        Else it will just return current path.
        """

        url_variants = ["http://youtu.be/", "https://youtu.be/", "http://youtube.com/", "https://youtube.com/",
                        "https://m.youtube.com/", "http://www.youtube.com/", "https://www.youtube.com/"]
        if any(ext in video_dir for ext in url_variants):
            print("Detected Youtube Video...")
            video_dir = Video.get_youtube_video(self.videoSaveDir, video_dir)
        return video_dir
