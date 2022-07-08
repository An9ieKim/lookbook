import json
import os
from collections import OrderedDict
import pandas as pd

fileName = "Lookbook_image_list_leaderboard.json" 
with open(fileName, "r", encoding="utf-8-sig") as openjson: 
    feeds = json.load(openjson)
    
    if type(feeds) is dict:
        feeds = [feeds]

#print(feeds[10]["ID"])
uniqueKey = []
img_list = []

newFile = "Lookbook_image_list_noDups.json"
img = OrderedDict()
with open(newFile, "w", encoding="utf-8-sig") as makeFile: #한글 깨질 때 인코딩 utf-8-sig 로 입력
     json.dump(img, makeFile, ensure_ascii=False, indent="\t")

print(type(feeds))

# for key in feeds.keys():
#     print(key)
#     print(feeds[key])


# for n in range(len(feeds)):
#     feeds[n]["joinkey"] = feeds[n]["ID"] + feeds[n]["postHead"] + feeds[n]["postDate"]



# for i in range(1, 20): #len(feeds)  
#     key = feeds[i]["joinkey"]
#     print(key)
    
#     if key not in uniqueKey:
#         uniqueKey.append(key)
#         FeedAdded = feeds[i]

#     #print(img_list)

#     with open(newFile, "w+", encoding="utf-8-sig") as open2json: #한글 깨질 때 인코딩 utf-8-sig 로 입력
#         img = json.load(open2json)
#         if type(img) is dict:
#             img = [img]
#         #print(feeds)
#     with open(newFile, "r+", encoding="utf-8-sig") as feeds2json: #한글 깨질 때 인코딩 utf-8-sig 로 입력
#         img.append(FeedAdded)
#         json.dump(img, feeds2json, ensure_ascii=False, indent="\t")
