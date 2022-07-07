from cProfile import Profile
import csv
from operator import itemgetter
from re import I
from time import time
from attr import attrs
import requests
from bs4 import BeautifulSoup
import numpy as np
import itertools


### Lookbook leaderboard에 있는 ID crawling (as of 5/31)
url = "https://lookbook.nu/leader/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
pageType=["today","this-week","this-month","this-year","all-time"]

### CSV파일 생성하여 account list 저장
filename = "Lookbook_account_list.csv"
f = open(filename, "w", encoding="utf-8-sig") #엑셀에서 파일 깨질때에는 인코딩 utf-8-sig 로 입력
writer = csv.writer(f)

title = ["Name","FullName","ProfileDesc","ID"] 
writer.writerow(title)


lst = []
for j in range(0, 5):
    res = requests.get(url + str(pageType[j]), headers=headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")
    
    profile = soup.find_all("li", attrs={"class":"topspaced"})

    for prof in profile:
        account = prof.find("a", attrs={"class":"no_underline"})
        desc = prof.find("p", attrs={"class":"grey less_linespaced least_topspaced lowercase force_wrap"})
        #print(account)
        prf = prof.get_text().splitlines()
        prf = list(filter(None, prf))
        #print(prf)

        Name = prf[0]
        #Karma = prf[1][1:len(prf[1])-1]
        ProfileDesc = desc.get_text()

        IDs = account["href"]
        fullName = account["title"]
        
        celeb = [Name, fullName, ProfileDesc, IDs]
        
        if celeb not in lst:
            lst.append(celeb)  

print(lst)
writer.writerows(lst)





