#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/17 12:29
# @Author : L
# @Software: PyCharm

import scrapy
import os
import requests
import json
from scrapy.http import Request
from bili_video.items import BiliVideoItem
import time
import random

user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class Myspider(scrapy.Spider):
    name='bili_video'
    allowed_domains=['https://apipc.app.acfun.cn']
    base_url='https://api.bilibili.com/'

    def start_requests(self):
        for x in range(1, 45000000):
            ua = random.choice(user_agent_list)
            self.headers = {
                'User-Agent': ua,
                'deviceType':0
            }
            url = "https://api.bilibili.com/x/web-interface/view?aid=%s" % x
            time.sleep(1)
            yield Request(url,headers=self.headers,callback=self.parse,meta={'url':url,'videoid':x})
    def parse(self,response):
        try:
            jsondata = json.loads(response.text)
            videoUrl = response.meta['url']
            idNum = response.meta['videoid']
            video = jsondata['data']
            pubdate = video['pubdate']
            uploadTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pubdate)))
            userName = video['owner']['name']
            videoCover = video['pic']
            videoTitle = video['title']
            playNum = video['stat']['view']
            danmuNum = video['stat']['danmaku']
            contenNum = video['stat']['reply']
            saveNum = video['stat']['favorite']
            coinNum = video['stat']['coin']
            likeNum = video['stat']['like']
            dislikeNum = video['stat']['dislike']
            shareNum = video['stat']['share']
            danmuID = video['cid']

            videos=video['videos']
            tid=video['tid']
            tname = video['tname']
            copyright = video['copyright']
            duration = video['duration']
            videoTitle=self.checkStr(videoTitle)
            userName=self.checkStr(userName)
            print('正在解析第%s条视频:%s'%(idNum,videoTitle))


            iterm=BiliVideoItem()
            iterm['videoTitle']=videoTitle
            iterm['videoUrl']=videoUrl
            iterm['videoCover']=videoCover
            iterm['userName']=userName
            iterm['uploadTime']=uploadTime
            iterm['playNum'] = playNum
            iterm['danmuNum'] = danmuNum
            iterm['contenNum'] = contenNum
            iterm['saveNum'] = saveNum
            iterm['coinNum'] = coinNum
            iterm['likeNum'] = likeNum
            iterm['dislikeNum'] = dislikeNum
            iterm['shareNum'] = shareNum
            iterm['danmuID'] = danmuID

            iterm['videos'] = videos
            iterm['tid'] = tid
            iterm['tname'] = tname
            iterm['copyright'] = copyright
            iterm['duration'] = duration



            yield iterm
        except Exception as e:
            # print('解析数据parse:%s'%e)
            return

    def checkStr(self,theStr):
        if '\\' in theStr:
            theStr = theStr.replace("\\", "\\\\")
        if "'" in theStr:
            theStr = theStr.replace("'", "\\'")
        if '"' in theStr:
            theStr = theStr.replace('"', '\\"')
        return theStr