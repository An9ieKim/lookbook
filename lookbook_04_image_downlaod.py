import json
from cProfile import Profile
import csv
import os
from operator import itemgetter
from re import I
from time import time
from time import sleep
from attr import attrs
import requests
import urllib.request as req
from bs4 import BeautifulSoup
import numpy as np
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from urllib.request import urlopen, urlretrieve, Request
import urllib.request 
from urllib.parse import urlparse

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

lst = []
fileName = "Lookbook_image_list.json" 
with open(fileName, "r", encoding="utf-8-sig") as openjson: 
    feeds = json.load(openjson)
    if type(feeds) is dict:
        feeds = [feeds]

# print(feeds[1023]["ImgName"])
# print(feeds[1023]["ImgSrc"])

 
n=1023
imgSrc = feeds[n]["ImgSrc"]
print(imgSrc)

with urlopen(imgSrc) as f:
    os.chdir('/Users/angiekim/Fashion_project/Lookbook/')
    req = Request(imgSrc, headers=headers)
    imgUrl = urlopen(req).read()
with open("/Users/angiekim/Fashion_project/Lookbook/img/" + str(feeds[n]["ImgName"]) + '.jpg','wb') as h:
    h.write(imgUrl)
 
# for n in range(0,2):
#     try:
#         imgSrc = print(feeds[n]["ImgSrc"])
#         print(imgSrc)
#         # if not urlparse(imgSrc).scheme:
#         #     imgSrc = 'http://' + imgSrc
#         # urlretrieve(imgSrc, '{}.jpg'.format(n))

#         with urlopen(imgSrc) as f:
#             os.chdir('/Users/angiekim/Fashion_project/Lookbook/')
#             req = Request(imgSrc, headers=headers)
#             imgUrl = urlopen(req).read()
#         with open("/Users/angiekim/Fashion_project/Lookbook/img/" + str(feeds[n]["ImgName"]) + '.jpg','wb') as h:
#             #img = f.read()
#             h.write(imgUrl)
#             #n += 1
#     except:
#         continue
