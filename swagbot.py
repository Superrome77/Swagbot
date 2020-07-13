import unittest
import time
import random
import selenium
import os
import pyautogui
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pickle

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
            with open("Swagcookies.txt", 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    print("cookie added")
                    self._driver.add_cookie(cookie)
            self._driver.get("https://www.swagbucks.com/")
        except Exception as e: 
            print(e)   
            print("Please sign in")
            time.sleep(120)
            with open("Swagcookies.txt", 'wb') as filehandler:
                pickle.dump(self._driver.get_cookies(), filehandler)
    def loadSurvey(self):
        self.print("------------------Load survey start-----------------------")
        for i in range(1):
            try:
                self._driver.get("https://www.swagbucks.com/surveys")
                surveys = self._driver.find_elements_by_xpath("//a[@class='surveyClick markClicked']")
                print(surveys)
                if len(surveys) == 1:
                    return None
                surveys[i].click()
                time.sleep(10)
                self.print("Survey found")
                self.execute()
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
            time.sleep(10)
            i = 1
            try:
                times = self._driver.find_elements_by_xpath("//p[@class='sbWatchPlaylistVideoTime']")
                for video in times:
                    duration = video.text
                    xx = duration.split(":")
                    if len(xx) == 1:
                        time.sleep(10)
                        print("broken")
                        return None
                    if len(xx) == 2:
                        minutes = int(xx[0])
                        seconds = int(xx[1])
                        total = (minutes*60 + seconds)
                    else:
                        seconds = int(xx[1])
                        total = (seconds)
                    print("total %i" %(total))
                    time.sleep(total)
                    time.sleep(random.randint(1,5))
                    nextVideo = self._driver.find_element_by_xpath("//a[@index='%i']" %(i))
                    nextVideo.click()
                    i += 1
                #time.sleep(90)
            except Exception as e:
                print(e)
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
                pyautogui.press("tab")
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
        submitWait = random.randint(1,2)
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
        time.sleep(2)
        self._actions.send_keys(Keys.DOWN)
        self._actions.send_keys(Keys.ENTER)
        self._actions.perform()
        self._actions.reset_actions()
        time.sleep(12)

    def print(self,string):
        print(string)
        self.filehandler.write("%s \n" %(string))

    def balance(self):
        self._driver.get("https://www.swagbucks.com/")
        balance = self._driver.find_element_by_xpath("//span[@id='sbBalance']")
        self.print("Balance is : %s" %(balance.text))
        self.print("__________________________________END______________________________________________")
        self._driver.close()
        pyautogui.keyDown('ctrl')
        pyautogui.press("c")
        pyautogui.keyUp('ctrl')

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

    def dailyDeal(self):
        try:
            self._driver.get("https://www.swagbucks.com/")
            time.sleep(2)
            self._driver.execute_script("window.scrollBy(0,100)")
            deal = self._driver.find_element_by_xpath("//*[contains(text(), 'Deal of the Day')]")
            deal.click()
            time.sleep(4)
        except:
            self.print("----------------------- Daily Deal not interactable ------------------------------")
            pass
        
    def search(self):
        terms = ["news","local news","weather","local weather","games","youtube","facebook","twitter","memes","twitter news","funny memes","funny","instagram","youtube trending","cats","games news","tumblr",
                "wikiHow","google","swagbucks","music","spotify","email","gamil","gmail","nwes","wether","utube","twiter","faecbook","stema","steam","redit","reddit","reddit old","reddit login","youtube login",
                "facebook login","twitter login","gmail login","netlfix","netflix","netflix login","twitch","twitch login","twithc","discrod","discord","discord login","amazon","ebay","yahoo","craiglist","maps",
                "google maps","google docs","google translate","cnn","hotmail","calculator","google drive","paypal","paypal login","zillow","entertainment","pintrest","speed test","roblox","linkedIn","amazon prime"
                "sports","hulu","pandora","etsy","nfl","just eat","deliveroo","imdb","expedia","123movies","outlook","gamestop","solitare","ikea","timer","date","art","deviantart","thesaurus","periodic table",
                "face","map","happy wheels","slitherio","calender","discover","movies","bitcoin","ip","audible","food","cars","google earth","amazon book","skype","firefox","online games","wikipedia","videos",
                "currency converter","webmd","shoes","miniclip","breaking news","dictionary","amazon uk","joji","post malone","top charts",
                
                "news","local nws","weathr","local eather","games","youtube","facebook","twitter","memes","twittr news","funy memes","fnny","instagram","youtube trening","cas","gmes news","tublr",
                "wikiow","gogle","swagbcks","music","spotiy","email","gamil","gail","nwes","wether","utube","twter","faecbok","stema","stam","redit","reddit","reddi old","reddit ogin","yoube login",
                "faceook login","twiter login","gmail logn","netlfix","netflix","netflix login","twitc","twich ogin","twihc","discrod","disord","discord login","amzon","ebay","ahoo","crailist","mps",
                "google maps","gogle dos","google tranlat","cnn","hotmail","calculator","google drive","paypl","paypal loin","zillow","entetainment","pintrest","sped test","robox","linkdIn","amazn prime"
                "sports","hulu","pandra","etsy","nfl","jut eat","deliveroo","imdb","expedia","123movies","otlook","gametop","solitare","ike","tier","date","art","eviantart","thsaurus","priodic tale",
                "face","ap","happywheels","sliherio","caender","discover","movies","bitcon","ip","audible","fod","cars","google earth","amazn book","skye","fiefox","online game","wikpedia","vidos",
                "currncy conveter","webd","shos","minilip","breaking news","dictionary","amazon uk","joji","pot malne","top charts"]
        while True:
            self._driver.get("https://search.swagbucks.com/")
            search = self._driver.find_element_by_xpath("//input[@type='text']")
            search.send_keys(terms[random.randint(0,len(terms)-1)])
            time.sleep(random.randint(5,8))
            enter = self._driver.find_element_by_xpath("//button[@id='sawSubmit']")
            enter.click()
            try:
                time.sleep(5)
                self._driver.find_element_by_xpath("//img[@id='captchaImg']")
                break
            except Exception as e:
                pass
            time.sleep(random.randint(60,90))
            print(self._driver.title)
        while True:
            time.sleep(15)
            if self._driver.title != "cp-claim-prize":
                pass
            else:
                break

if __name__ == "__main__":
    rounds = 0
    t = SeleniumTest()
    t.banner()
    t.flash()
    t.daily()
    t.profileSurvey()
    t.daily()
    t.game()
    t.profileSurvey()
    t.game()
    t.watch("https://www.swagbucks.com/watch/playlists/3/food?sort=8")
    for i in range(30):
        t.game()
        time.sleep(60)
    t.balance()
    t.log()
    sys.exit()