from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bot:
    """Bot used as high level interaction with web-browser via Javascript exec"""
    def __init__(self, bot):
        self.bot = bot

    def getBot(self):
        return self.bot

    def getVideoUploadInput(self):
        # Button is nested in iframe document. Select iframe first then select upload button
        WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.bot.switch_to.frame(0)
        #file_input_element = self.bot.find_elements(By.CLASS_NAME, "upload-btn-input")[0]
        file_input_element = WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        # document.getElementsByClassName("op-part")[0].childNodes[1]  # New locator
        return file_input_element

    def getNewestVideoHref(self):
        WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.XPATH, "//div[@data-e2e='user-post-item-list']")))
        top_video_element = self.bot.find_elements(By.XPATH, "//div[@data-e2e='user-post-item']")[0]
        return top_video_element.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a").get_attribute("href")

    def getCaptionElem(self):
        #self.bot.execute_script(f'var element = document.getElementsByClassName("public-DraftStyleDefault-block")[0].children[0].getAttribute("data-offset-key");')
        #caption_elem = self.bot.find_elements(By.CLASS_NAME, "public-DraftStyleDefault-block")[0]
        caption_elem = WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "public-DraftStyleDefault-block")))
        return caption_elem

    def uploadButtonClick(self):
        upload_elem = self.bot.find_element(By.CLASS_NAME, "btn-post")
        #print(upload_elem.is_enabled())
        WebDriverWait(self.bot, 50).until(EC.invisibility_of_element_located((By.XPATH, "//button[@disabled]")))
        upload_elem.click()

    def waitUntilUploaded(self):
        # Must switch frames or something first, otherwise not found
        WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.XPATH, "//div[@id='portal-container']")))
        WebDriverWait(self.bot, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-title")))
