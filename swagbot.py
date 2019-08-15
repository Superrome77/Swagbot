import unittest
import time
import random
import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pickle
from FacebookBot import SeleniumTest as logon

class SeleniumTest():
    def __init__(self):
        self.filehandler = open("log.txt","r+")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--mute-audio")
        prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://www.swagbucks.com"
        }
        options.add_experimental_option("prefs",prefs)
        self._driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
        #self._driver = webdriver.Firefox(executable_path="C:\\Users\\soconnel\\Downloads\\geckodriver.exe")
        self._actions = ActionChains(self._driver)
        #self._driver.set_window_size(1550,2000)
        self._driver.get("https://www.swagbucks.com/")
        try:
            with open("cookies.txt", 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self._driver.add_cookie(cookie)
            self._driver.get("https://www.swagbucks.com/")
        except:
            time.sleep(120)
            with open("cookies.txt", 'wb') as filehandler:
                pickle.dump(self._driver.get_cookies(), filehandler)
    def loadSurvey(self):
        self.print("------------------Load survey start-----------------------")
        for i in range(10):
            try:
                self._driver.get("https://www.swagbucks.com/surveys")
                surveys = self._driver.find_elements_by_xpath("//a[@class='surveyClick markClicked']")
                surveys.click[i]
                time.sleep(10)
                self.print("Survey found")
                execute()
            except:
                self.print("No survey found")
                pass
    def game(self):
        self.print("------------------Game start-----------------------")
        self._driver.get("https://www.swagbucks.com/games/play/114/swagasaurus-run")
        time.sleep(2)
        play = self._driver.find_element_by_xpath("//a[@class='gamesBtn gamesBtnGreen']")
        play.click()
        self.print("Loading game")
        time.sleep(10)
        game = self._driver.find_element_by_xpath("//div[@id='embedContainer']")
        game.click()
        self.print("game loaded")
        for i in range(3):
            self._actions.send_keys(Keys.TAB)
            self._actions.send_keys(Keys.ENTER)
            self._actions.perform()
            self._actions.reset_actions()
        self.print("Game started")
        time.sleep(10)
        while True:
            self._driver.switch_to.window(self._driver.window_handles[len(self._driver.window_handles)-1])
            if len(self._driver.window_handles) != 1:
                self._driver.close()
            else:
                self.print("Windows closed")
                break

    def watch(self,url):
        for i in range(10):
            self.print("------------------Watch start-----------------------")
            time.sleep(2)
            self._driver.get(url)
            time.sleep(2)
            videos = self._driver.find_elements_by_xpath("//span[@class='sbTrayListItemSbEarn sbColor4']")
            self.print("videos available: %i " %(len(videos)))
            watched = self._driver.find_elements_by_xpath("//p[@class='playlistWasWatched']")
            self.print("videos watched: %i " %(len(watched)))
            if len(videos) == len(watched):
                self.print("all videos watched")
                return None
            for i in range(20):
                try:
                    videos[0 + len(watched)].click()
                    break
                except:
                    pass
            self.print("Playlist selected")
            time.sleep(3)
            for i in range(50):
                try:
                    nextVideo = self._driver.find_element_by_xpath("//a[@index='%i']" %(i))
                    nextVideo.click()
                    self.print("video playing")
                    time.sleep(80)
                except Exception as e:
                    print("end of playlist")
                    pass
            time.sleep(2)


    def daily(self):
        self.print("------------------Daily survey start-----------------------")
        try:
            self._driver.get("https://www.swagbucks.com/polls")
            time.sleep(2)
            self.answer()
            self.submit()
            time.sleep(2)
            self.print("Daily answered")
        except Exception as e:
            self.print("Daily already answered")
            pass

    def profileSurvey(self):
        self.print("------------------Profile survey start-----------------------")
        count = 0
        self._driver.get("https://www.swagbucks.com/surveys")
        while True:
            try:
                time.sleep(2)
                if count == 10:
                    self.print("No available profile questions")
                    return None
                drop = self._driver.find_element_by_xpath("//span[@class='surveyDropdownVal']")
                drop.click()
                time.sleep(3)
                dropAnswerRand = random.randint(0,4)
                dropAnswer = self._driver.find_element_by_xpath("//span[@data-index='%i']" %(dropAnswerRand))
                dropAnswer.click()
                time.sleep(1)
                self._actions.send_keys(Keys.TAB)
                self._actions.send_keys(Keys.ENTER)
                self._actions.perform()
                self._actions.reset_actions()
                self.print("Profile question answered")
                count = 0
                time.sleep(3)
            except:
                count += 1
                pass



    def answer(self):
        time.sleep(1)
        answers = self._driver.find_elements_by_xpath("//td[@class='pollMainAnswerText']")
        rand = random.randint(0,len(answers)-1)
        answers[rand].click()
    def submit(self):
        time.sleep(1)
        submit = self._driver.find_element_by_xpath("//div[@id='btnVote']")
        submit.click()

    def execute(self):
        self.print("Starting survey")
        for i in range(1000):
            try:
                radios = self._driver.find_elements_by_xpath("//input[@type='radio']")
                for r in radios:
                    r.click()
                    randomint = random.randint(0,len(radios)-1)
                    radios[randomint].click()
                    self.print("Radio button found")
            except:
                self.print("No radio buttons found")
                pass
            try:
                spans = self._driver.find_elements_by_tag_name("span")
                for s in spans:
                    s.click()
                    randomint = random.randint(0,len(spans)-1)
                    spans[randomint].click()
                    self.print("Span found")
            except:
                self.print("No span found")
                pass
            try:
                labels = self._driver.find_elements_by_tag_name("label")
                for l in labels:
                    l.click()
                    randomint = random.randint(0,len(labels)-1)
                    labels[randomint].click()
                    self.print("Span found")
            except:
                self.print("No label found")
                pass
            try:
                texts = self._driver.find_elements_by_xpath("//input[@type='text']")
                for t in texts:
                    t.click()
                    randomtext = random.randint(0,2000)
                    t.send_keys("%i" %(randomtext))
                    self.print("Text box found")
            except:
                self.print("No text box found")
                pass
            self.print("----Submitting answer----")
            self.surveySubmit()

    def surveySubmit(self):
        submitWait = random.randint(10,30)
        time.sleep(submitWait)
        try:
            surveySubmit = self._driver.find_elements_by_xpath("//input[@type='submit']")
            self.print("Submit button found")
            for ss in surveySubmit:
                ss.click()
                self.print("Answer submitted")
                try:
                    test = self._driver.find_element_by_tag_name("body")
                except:
                    time.sleep(1)
                    self.print("Searching for page")
                    pass
        except:
            self.print("No Submit button found")
            pass

    def flash(self):
        self.print("------------------Flash enable start-----------------------")
        self._driver.get("chrome://settings/content/siteDetails?site=https%3A%2F%2Fwww.swagbucks.com")
        time.sleep(2)
        for i in range(10):
            self._actions.send_keys(Keys.TAB)
            self._actions.perform()
            self._actions.reset_actions()
        self._actions.send_keys(Keys.ENTER)
        self._actions.send_keys(Keys.TAB)
        self._actions.send_keys(Keys.ENTER)
        self._actions.perform()
        self._actions.reset_actions()
        time.sleep(2)
        self._actions.send_keys(Keys.DOWN)
        self._actions.send_keys(Keys.ENTER)
        self._actions.click()
        self._actions.perform()
        self._actions.reset_actions()
        time.sleep(2)
        self.print("Flash enabled")

    def print(self,string):
        print(string)
        self.filehandler.write("%s \n" %(string))

    def balance(self):
        self._driver.get("https://www.swagbucks.com/")
        balance = self._driver.find_element_by_xpath("//span[@id='sbBalance']")
        self.print("Balance is : %s" %(balance.text))
        self.print("__________________________________END______________________________________________")

    def banner(self):
        try:
            banner = self._driver.find_element_by_xpath("//button[@class='bannerClose black bannerCloseCustom']")
            banner.click()
        except:
            pass

    def watch2(self):
        self.print("-----------------------3rd party watch start----------------------")
        for i in range(3):
            try:
                self._driver.get("https://www.swagbucks.com/discover/offer-walls/138/adscendmedia")
                time.sleep(3)
                frame = self._driver.find_element_by_xpath("//iframe[@id='wallIframe']")
                self._driver.switch_to.frame(frame)
                videos = self._driver.find_element_by_xpath("//div[@data-value='19']")
                videos.click()
                time.sleep(3)
                buttons = self._driver.find_elements_by_xpath("//*[contains(text(), '+2')]")
                #print(buttons)
                #buttons = self._driver.find_elements_by_xpath("//*[contains(text(), '+1')]")
                print(buttons)
                time.sleep(2)
                title = buttons[i].get_attribute("href")
                self._driver.switch_to.default_content()
                self._driver.get(title)
                time.sleep(7)
                play = self._driver.find_element_by_xpath("//div[@itemprop='video']")
                play.click()
                for k in range(50):
                    time.sleep(10)
                    try:
                        close = self._driver.find_element_by_xpath("//a[@title='Close']")
                        close.click()
                        print("closed")
                        play = self._driver.find_element_by_xpath("//div[@itemprop='video']")
                        #play.click()
                    except:
                        pass
                    try:
                        finish = self._driver.find_element_by_xpath("//button[@id='finish_offer']")
                        finish.click()
                    except:
                        pass
                time.sleep(4)
            except:
                pass
    def watch3(self):
        for i in range(11):
            try:
                self._driver.get("https://www.swagbucks.com/discover/offer-walls/138/adscendmedia")
                time.sleep(3)
                frame = self._driver.find_element_by_xpath("//iframe[@id='wallIframe']")
                self._driver.switch_to.frame(frame)
                videos = self._driver.find_element_by_xpath("//div[@data-value='19']")
                videos.click()
                time.sleep(3)
                buttons = self._driver.find_elements_by_xpath("//*[contains(text(), '+1')]")
                print(buttons)
                time.sleep(2)
                title = buttons[i].get_attribute("href")
                self._driver.switch_to.default_content()
                self._driver.get(title)
                time.sleep(7)
                play = self._driver.find_element_by_xpath("//div[@itemprop='video']")
                play.click()
                for k in range(10):
                    time.sleep(10)
                    try:
                        close = self._driver.find_element_by_xpath("//a[@title='Close']")
                        close.click()
                        print("closed")
                        play = self._driver.find_element_by_xpath("//div[@itemprop='video']")
                        #play.click()
                    except:
                        pass
                    try:
                        finish = self._driver.find_element_by_xpath("//button[@id='finish_offer']")
                        finish.click()
                    except:
                        pass
                time.sleep(4)
            except:
                pass
        reward = self._driver.find_element_by_xpath("//button[@id='rewards']")
        reward.click()
        claim = self._driver.find_element_by_xpath("//button[@class='enter-promo-btn promo-code-js']")
        claim.click()
if __name__ == "__main__":
    rounds = 0
    t = SeleniumTest()
    """
    t.banner()
    t.flash()
    t.game()
    t.daily()
    t.game()
    t.profileSurvey()
    t.game()
    #t.watch("https://www.swagbucks.com/watch/playlists/333/news-politics?sort=8")
    #t.game()
    """
    t.watch3()
    """
    t.watch("https://www.swagbucks.com/watch/playlists/3/food?sort=8")
    for i in range(30):
        t.game()
        time.sleep(60)
    t.balance()
    t.log()
    """