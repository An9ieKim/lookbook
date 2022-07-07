import csv
from operator import itemgetter
from re import I
from time import time
from time import sleep
from urllib.error import HTTPError, URLError
from attr import attrs
import requests
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

### Followr ID list 만들기
filename = "Lookbook_account_list.csv"
f = open(filename, "w", encoding="utf-8-sig") #엑셀에서 파일 깨질때에는 인코딩 utf-8-sig 로 입력
writer = csv.writer(f)

title = ["Name","FullName","ProfileDesc","ID"] 
writer.writerow(title)

followerList = []

### Influecer 계정 페이지 들어가서 lookbook image & info scraping
for account in range(len(lst)):
    print(account)
    #followerList = []
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
    options.add_argument('headless')
    options.add_argument("disable-gpu")

    browser = webdriver.Chrome('/Users/angiekim/Fashion_project/Lookbook/chromedriver',chrome_options=options)
    browser.get(url) # url로 이동
    try:
        browser.find_element(by=By.XPATH, value='//*[@id="main_col"]/nav/div[1]/ul/li[6]/a').click() #following 버튼 클릭
    except:
        browser.quit()
        continue
    sleep(3)

    res = requests.get(browser.current_url, headers=headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")

    follows = soup.find_all("td",attrs={"style":"padding:14px 36px 14px 8px;"})
    for follow in enumerate(follows):
        name = follow[1].find("a")["title"]
        fullName = follow[1].find("a").get_text()
        accountID = follow[1].find("a")["href"]
        profDesc = follow[1].find("p").text.strip()
        followers = [name, fullName, profDesc, accountID]
        
        if followers not in followerList:
            followerList.append(followers) 
        browser.quit()    

writer.writerows(followerList)    
browser.quit()
