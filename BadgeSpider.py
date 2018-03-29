#-*- coding: UTF-8 -*-
import json
import requests
from bs4 import BeautifulSoup
from urllib import request

#---------------获取大学信息，将对应大学url储存在Urllist中-----------------------------------
fo = open("/Users/mac/Desktop/CodeSpace/SchoolRush/Campus.json", encoding="utf-8")
Campusdict = json.load(fo)
Campuslist = []
Urllist = []

for key in Campusdict:
    for campu in Campusdict[key]:
        Campuslist.append(campu['value'])
for campu in Campuslist:
    temp1 = campu.find('(')
    temp2 = campu.find(')')
    if temp1 != -1 & temp2 != -1:
        url = 'https://baike.baidu.com/item/'+campu[0:temp1]+'（'+campu[temp1+1:temp2]+'）'
        Urllist.append(url)

    else:
        url = 'https://baike.baidu.com/item/'+campu
        Urllist.append(url)



#---------------------------------------------------------------------------------------
#---------------------Badge Spider------------------------------------------------------
# 无法直接请求的url = 41

heads = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
UCurl = []

#img格式选择函数
def getImgUrl(a = [], b = []):
    if(a == []):
        return b
    else:
        return a

for url in Urllist:
    num = 0
    response = requests.get(url, allow_redirects=False, headers=heads[num % len(heads)])
    #判断请求的 url 是否有效
    if response.status_code == 200:
        response.encoding = ('utf-8')#将请求到的页面转码
        html = response.text #请求的 url 的 html 代码
        soup = BeautifulSoup(html, 'html.parser') #用html.parser对网页解析

        img1 = soup.select('body > div.body-wrapper.feature.feature_small.collegeSmall > div.feature_poster > div > div.poster-right > div > a > img')
        #                  body > div.body-wrapper.feature.feature_small.collegeSmall > div.feature_poster > div > div.poster-right > div > a > img
        #                  body > div.body-wrapper > div.content-wrapper > div > div.side-content > div.summary-pic > a > img
        #------------------body > div.body-wrapper > div.content-wrapper > div > div.side-content > div.summary-pic > a > img
        # 选择校徽图片的位置，得到校徽块相关信息
        img2 = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.side-content > div.summary-pic > a > img')
        #由于百度百科的 badge 图片的html格式有所不同，但基本为这两个格式，所以添加两个img格式

        img = getImgUrl(img1, img2)

        #print(img)

        if img == []:
            with open('unfinishedURL.txt', 'a') as fo:
                fo.writelines(url)
                fo.writelines('\n')
            continue

        img_url = img[0].get_attribute_list('src')[0]#获取校徽图片地址
        #将获得的校徽图片保存本地
        pic = requests.get(img_url)
        path = 'Badges/'+url[29:]+'.jpg'
        with open(path, 'wb') as fp:
            fp.write(pic.content)
    #url 地址请求失败时，将失败的URL存入 unfinishedURL 文本中
    else:
        with open('unfinishedURL.txt', 'a') as fo:
            fo.writelines(url)
            fo.writelines('\n')
    num = num + 1
    print(url)

print("OK!Well Done!")





