from selenium import webdriver
import requests
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
wait = WebDriverWait(driver,5)
        

base_url = [
'https://www.youtube.com/c/AshleySmithTV/',
'https://www.youtube.com/channel/UC0uHB4d6u0jIJSgPC3WzBFw/',
'https://www.youtube.com/c/msbrittanysarah/',
'https://www.youtube.com/c/vasseurbeauty/',
'https://www.youtube.com/user/cammie919/',
'https://www.youtube.com/channel/UCRXoGyLligcyVA1UWVV0cNg/',
'https://www.youtube.com/channel/UCvkCXERHO-0u5AW2wuzEXWA/',
'https://www.youtube.com/channel/UCDBroOWVP4aN8SYM0br6sJQ/',
'https://www.youtube.com/user/emilynorrisloves/',
'https://www.youtube.com/channel/UC3w9E1N7zukLxJ5bkrU4IKw/',
'https://www.youtube.com/channel/UC7fPf1yuGaYFmbxe0ZrshWw/',
'https://www.youtube.com/c/JettingJulia/',
'https://www.youtube.com/channel/UCP1odR9n2-qGsRdVXIkJqwg/,'
'https://www.youtube.com/channel/UCsxYHogcRJlu-xXFjggC0JA/',
'https://www.youtube.com/c/vlogwithkendra/',
'https://www.youtube.com/channel/UCwEq1lQikxTIjO61JlbHc7Q/',
'https://www.youtube.com/user/PrincessLaurenTV/',
'https://www.youtube.com/channel/UCWoEpiHaC7LOQhaHFT8Rx7A/',
'https://www.youtube.com/c/LisaOnuoha/',
'https://www.youtube.com/c/MaggieMacDonaldVlogs/',
'https://www.youtube.com/c/MissMikaylaG/',
'https://www.youtube.com/c/NadiaAnya/',
'https://www.youtube.com/c/NatalieBarbu/',
'https://www.youtube.com/c/PaytonSartainHH/',
'https://www.youtube.com/c/RisaDoesMakeup/',
'https://www.youtube.com/c/tarahenderson/',
'https://www.youtube.com/c/glamtwinz334/',
'https://www.youtube.com/c/valelorenbeautychannel/',
'https://www.youtube.com/channel/UC63MviKbxyCP7Yw6wxW5JAw/',
'https://www.youtube.com/c/AjaDang/',]

def scroll_down():
    time.sleep(.5)
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    time.sleep(.3)
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    time.sleep(.3)
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def Likes():
        if  check_exists_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string') == True:
            likes = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').text                              
            if "LIKE" in likes:
                likes = likes.rstrip("LIKE")
                likes = 0
                return likes
            elif  "K" in likes:
                likes = likes.rstrip("K")
                likes = float(likes) *1000
                likes = int(likes)
                return likes
            else:
                try:
                    likes = int(likes)
                    return likes
                except ValueError:   
                    likes = 0
                    print("likes sckiped")
                    return likes

def Dislikes():
    dislik = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string').text                              
    dislik = dislik.rstrip("K")
    dislik = dislik.rstrip("DISLIKE")

    try:
        dislik = float(dislik)
        dislik = float(dislik)
        return dislik
    except ValueError:
        dislik = 0
        return dislik

def Comments():
    retry = 0
    while True:
        try:
            print("comments")
            scroll_down()
            time.sleep(2)
            pres = EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]'))
            WebDriverWait(driver,5).until(pres)
            com = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]').text
            com = int(com.replace(',',''))
            return com
            break
        except TimeoutException:
            retry += 1
            if retry == 2:
                com = 0
                return com
                break
            else:
                driver.refresh()
                scroll_down()
            



stats = []

for url in base_url:
        rerunlike = 0
        rerundislike = 0
        reruncom = 0
        about_url = url+'about'
        driver.get(about_url)
        views = driver.find_elements_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]')
        subs = driver.find_elements_by_xpath('//*[@id="subscriber-count"]')
        channel = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/ytd-channel-name/div/div/yt-formatted-string').text
        for p in range(len(views)):
            views = views[p].text.rstrip(" views")
            print("Views Gathered")
        for p in range(len(subs)):
            if "K" in subs[p].text:
                subs = subs[p].text.rstrip("K subscribers")
                subs = float(subs)*1000
                print("Subs Gathered")
            else:
                if "M" in subs[p].text:
                    subs = subs[p].text.rstrip("M subscribers")
                    subs = float(subs)*1000000
                    print("Subs Gathered")

        vid_url = url+'videos'
        driver.delete_all_cookies()
        driver.get(vid_url)
        for x in range(50):
            driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
            time.sleep(.1)
            driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    
        hrefs = driver.find_elements_by_xpath('//*[@id="video-title"]')
        print("HREF gathered")

        href_list =[]
        for p in hrefs:
            href = p.get_attribute('href')
            href_list.append(href)
            lcount = 0
            dcount = 0
            ccount = 0
            pcount = 0
        for href in href_list:
            driver.delete_all_cookies()
            driver.get(str(href))
            time.sleep(3)
            
            if  check_exists_by_xpath('/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/yt-live-chat-header-renderer/div[1]/span[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/div/tp-yt-paper-button/div')  ==  True:
                print("Skipped")
                lcount = lcount + 0
                dcount = dcount + 0
                ccount = ccount + 0
                pcount = pcount + 1
                break
            
            else:
                likes = Likes()
                dislike = int(Dislikes())
                comments = int(Comments())
                lcount = lcount + likes
                dcount = dcount + dislike
                ccount = ccount + comments
                pcount = pcount + 1
                postcount = len(href_list)
                print(channel,": ",pcount,"/",postcount)
                print("Likes: ",lcount," ","Dislikes: ",dcount," ","Comments: ",ccount)

                
        stat = {"Channel":channel, "Subs":subs,"Views":views,"Posts":pcount,"Likes":lcount,"Dislikes":dcount,"Comments":ccount }
        stats.append(stat)
        dp = pd.DataFrame(stats)
        dp.to_csv("stat.csv")
        print("stat file done")



df = pd.DataFrame(stats)
df.to_csv("youtube.csv")
print("Done go check file")


                    
