import json

fileName = "Lookbook_image_list.json" 
 
with open(fileName, "r", encoding="utf-8-sig") as openjson: #한글 깨질 때 인코딩 utf-8-sig 로 입력
    feeds = json.load(openjson)
    if type(feeds) is dict:
        feeds = [feeds]
    print(len(feeds))