from ast import Continue
from cProfile import Profile
import csv
from operator import itemgetter
from re import I
from time import time
from time import sleep
from urllib.error import HTTPError, URLError
from attr import attrs
from pyrsistent import v
import requests
import json
from collections import OrderedDict
import urllib.request as req
from bs4 import BeautifulSoup
import numpy as np
import itertools
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains

### Inflencer ID list 열기
lst = []
csv_file = open("./Lookbook_account_list.csv", "r", encoding="utf-8-sig", errors="", newline="" ) 
rdr = csv.reader(csv_file) 
for line in rdr:
    lst.append(line)

### Image list Json file 생성 (제일 처음 한번 돌릴때에만 사용)
fileName = "Lookbook_image_list.json" 
# imageData = OrderedDict()
# with open(fileName, "w", encoding="utf-8-sig") as makeFile: #한글 깨질 때 인코딩 utf-8-sig 로 입력
#     json.dump(imageData, makeFile, ensure_ascii=False, indent="\t")


### Influecer 계정 페이지 들어가서 demographic & image & info scraping
for account in range(221,len(lst)): #len(lst)
    print(account)
    url = "https://lookbook.nu/" + str(lst[account][3])
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}

    res = requests.get(url, headers=headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")

    options = webdriver.ChromeOptions()
    options.add_argument("Start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    options.add_argument("disable-gpu")
    options.add_argument('headless')

    browser = webdriver.Chrome('/Users/angiekim/Fashion_project/Lookbook/chromedriver',chrome_options=options)
    browser.get(url) # url로 이동

    # demographic 정보 스크랩
    idAccount = str(lst[account][3])
    try:
        fullName = soup.find("a", attrs={"class":"no_underline"}).get_text()
    except:
        fullName = ""
    try:
        profDesc = soup.find("p", attrs={"class":"byline"}).get_text().strip()
    except:
        profDesc = ""
    try:
        profStat = soup.find("ul", attrs={"class":"profile_stats"}).get_text().split()
    except:
        profDesc = ""
    fansCnt = int(profStat[0].replace(',',''))
    looksCnt = int(profStat[2].replace(',',''))
    likesCnt = int(profStat[4].replace(',',''))
    karmaCnt = int(profStat[5].replace(',',''))
    commentsCnt = int(profStat[11].replace(',',''))
    commentKarmaCnt = int(profStat[13].replace(',',''))
    
    try:
        genderChk = soup.find("div", attrs={"class":"right rightspaced"}).find("img", attrs={"itemprop":"image"})["onerror"]
        if "girl" in genderChk:
            gender = "Female"
        else:
            gender = "Male"
    except:
        gender = ""

    ### Looks 페이지 열기
    try:
        browser.find_element(by=By.XPATH, value='//*[@id="main_col"]/nav/div[1]/ul/li[2]/a').click() #looks 버튼 클릭
    except:
        browser.quit()
        continue
    sleep(3)

    ### 첫번째 사진 클릭해서 상세 팝업 페이지 열기
    try:
        browser.find_element(by=By.CLASS_NAME, value='look-photo').click() 
        browser.implicitly_wait(3)
    except:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    browser.implicitly_wait(3)
    res = requests.get(browser.current_url, headers=headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")

    tags = []
    items = []

    # 이미지 상세 페이지에서 이미지 & 정보 크롤링
    for i in range(looksCnt):
        try:  
            ImgSrc = "http:" + soup.find("img",attrs={"id":"main_photo"})["src"]
            postHead = soup.find("div",attrs={"class":"look-meta-container"}).get_text().strip().splitlines()[0]
            try:
                postContent = soup.find("p",attrs={"id":"look_descrip"}).get_text().strip('/n').split("#")[0]
            except:
                postContent = [None]
            try:
                tagList = soup.find("p",attrs={"id":"look_descrip"}).get_text().strip('/n').split("#")[1:]
            except:
                tagList = [None]
            postDate = soup.find("meta",attrs={"itemprop":"dateCreated"})["content"]
            hypeCnt = soup.find("div",attrs={"class":"hypes-count"}).get_text()
            commentsCnt =  soup.find("p",attrs={"class":"look-stats"}).get_text().split()[-1]
            ImgName = str(str(idAccount) + "_" + str(i) + "_" + postDate + "_" + postHead)
            items = []
            itemName = soup.find_all("div",attrs={"class":"item-info"})

            for j in itemName:
                item = j.get_text().strip()#.split()
                items.append(item)
                
            #json 파일추가
            imageData = OrderedDict()
            imageData["ID"] = idAccount
            imageData["FullName"] = fullName
            imageData["ProfDesc"] = profDesc
            imageData["Gender"] = gender
            imageData["Locality"] = profDesc.split('from')[-1].strip()
            imageData["Country"] = profDesc.split('from')[-1].strip().split(',')[-1].strip()
            imageData["FansCnt"] = fansCnt
            imageData["LooksCnt"] = looksCnt
            imageData["LikesCnt"] = likesCnt
            imageData["ImgName"] = ImgName
            imageData["ImgSrc"] = ImgSrc
            imageData["postHead"] = postHead
            imageData["postContent"] = postContent
            imageData["postDate"] = postDate
            imageData["tagList"] = tagList
            imageData["hypeCnt"] = hypeCnt
            imageData["commentsCnt"] = commentsCnt
            imageData["items"] = items

            browser.implicitly_wait(5)
            
            with open(fileName, "r", encoding="utf-8-sig") as openjson: #한글 깨질 때 인코딩 utf-8-sig 로 입력
                feeds = json.load(openjson)
                if type(feeds) is dict:
                    feeds = [feeds]
                #print(feeds)
            with open(fileName, "r+", encoding="utf-8-sig") as feedsjson: #한글 깨질 때 인코딩 utf-8-sig 로 입력
                feeds.append(imageData)
                json.dump(feeds, feedsjson, ensure_ascii=False, indent="\t")

            browser.implicitly_wait(5)

            # 다음 사진으로 이동
            try:
                element = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.ID, "next_look"))
                    )
                browser.find_element(by=By.ID, value='next_look').click()
                res = requests.get(browser.current_url, headers=headers)
                res.raise_for_status
                soup = BeautifulSoup(res.text, "lxml")
            except:
                browser.refresh()
                break
        except:
            browser.quit()
            continue         

        
    browser.quit()
browser.quit()