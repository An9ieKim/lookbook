import urllib
import urllib.request
from urllib.request import urlopen, urlretrieve, Request
import json
import os

# 이미지 리스트 JSON 파일 열기
fileName = "Lookbook_image_list_leaderboard.json" 
with open(fileName, "r", encoding="utf-8-sig") as openjson: 
    feeds = json.load(openjson)
    if type(feeds) is dict:
        feeds = [feeds]

# 이미지 URL로 다운로드 후 img폴더에 저장
headers = {'User-Agent': 'Mozilla/5.0'}
table = str.maketrans('\/:*?"<>|','         ')
imgList = []
print(type(feeds))

# for n in range(1,2000):
#     try:
#         if n % 5 ==0: print(n)
#         imgUrl = feeds[n]["ImgSrc"]
#         imgName = feeds[n]["ImgName"].translate(table)
#         req = Request(imgUrl, headers=headers)

#         if imgName not in imgList:  
#             with urlopen(req) as f:
#                 with open('./img/' + str(feeds[n]["ImgName"])+'.jpg','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
#                     img = f.read() #이미지 읽기
#                     h.write(img) # 이미지 저장
#             imgList.append(imgUrl)
#     except:
#         continue
