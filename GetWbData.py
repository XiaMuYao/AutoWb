#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/2/26 21:56 
# @Author : 夏沐尧 
# @Site :  
# @File : GetWbData.py
# @Software: PyCharm

import json
import re

import sys
from imp import reload

# reload(sys)
# sys.setdefaultencoding('utf-8')

from pip._vendor import requests

from threading import Thread

headers = {
    'User-Agent': 'Mozillhttps://m.weibo.cn/u/3217179555?uid=3217179555&luicode=20000174a/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}
headers1 = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
}


# 多进程注解
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def huoqu(WbId):
    nowPageNum = 1
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + WbId + '&page=' + str(
            nowPageNum)
        # 发起请求
        response = requests.get(url, headers=headers)
        print(response.text)
        # 返回数据解析成json格式
        mjson = json.loads(response.text)
        # 如果data>0 说明请求成功并且有数据
        if (len(mjson['data']) > 0):
            if ((mjson['ok']) == 1):
                # 在这里进行数据页数增加
                nowPageNum = nowPageNum + 1
            elif ((mjson['ok']) == 0):
                return "数据完成 当前页数" + str(nowPageNum)
            for mblogIndex in range(0, len(mjson['data']['cards'])):
                if (len(mjson['data']['cards'][mblogIndex]) > 4):
                    # 用户说话
                    re_talktext = mjson['data']['cards'][mblogIndex]['mblog']['text']
                    # 这里使用个正则过滤掉了标签内容
                    # dr = re.compile(r'<[^>]+>', re.S)
                    # Db_talktext = dr.sub('', re_talktext)
                    Db_talktext = str(re_talktext).replace("\"", '\'')
                    # 用户名字
                    Db_name = mjson['data']['cards'][mblogIndex]['mblog']['user']['screen_name']
                    Db_name = "\"" + Db_name + "\""
                    # 用户id
                    Db_id = mjson['data']['cards'][mblogIndex]['mblog']['user']['id']
                    Db_id = str(Db_id)
                    Db_id = '\"' + Db_id + '\"'
                    # 用户时间
                    Db_time = mjson['data']['cards'][mblogIndex]['mblog']['created_at']
                    Db_time = "\"" + Db_time + "\""
                    # 用户图片
                    Db_picList = []
                    try:
                        for i in range(0, len(mjson['data']['cards'][mblogIndex]['mblog']['pics'])):
                            Db_picList.append(
                                mjson['data']['cards'][mblogIndex]['mblog']['pics'][i][
                                    'url'])
                    except:
                        Db_picList = []
                    str2 = ','.join(str(i) for i in Db_picList)
                    Db_picListStr = str2
                    # 用户视频
                    try:
                        Db_Video = \
                            mjson['data']['cards'][mblogIndex]['mblog']['page_info']['media_info'][
                                'stream_url']
                    except:
                        Db_Video = ""
                        # ----------------------------------------------------------------------------------
                        # 判断是否存在转发数据
                        try:
                            Db_forwardData = mjson['data']['cards'][mblogIndex]['mblog'][
                                'retweeted_status']

                            # 转发得文字
                            Db_forTest = Db_forwardData['text']
                            dr = re.compile(r'<[^>]+>', re.S)
                            Db_forTest = dr.sub('', Db_forTest)
                            # Db_forTest = Db_forTest

                            # 被转发者名字
                            Db_forname = Db_forwardData['user']['screen_name']
                            Db_forname = "\"" + Db_forname + "\""

                            # 被转发者Id
                            Db_forid = Db_forwardData['user']['id']
                            Db_forid = str(Db_forid)
                            Db_forid = '\"' + Db_forid + '\"'

                            # 被转发者用户时间
                            Db_fortime = Db_forwardData['created_at']
                            Db_fortime = "\"" + Db_fortime + "\""

                            # 被转发者图片
                            Db_forpicList = []
                            try:
                                for i in range(0, len(Db_forwardData['pics'])):
                                    Db_forpicList.append(
                                        Db_forwardData['pics'][i][
                                            'url'])
                            except:
                                Db_forpicList = []
                            Db_forstr2 = ','.join(str(i) for i in Db_forpicList)
                            Db_forpicListStr = Db_forstr2

                            # 用户视频
                            try:
                                Db_forVideo = \
                                    Db_forwardData['page_info']['media_info'][
                                        'stream_url']
                            except:
                                Db_forVideo = ""
                            print("转发得数据" + "转发得文字---" + Db_forTest, "转发的姓名" + Db_forname,
                                  "转发的id" + Db_forid, "转发的时间" + Db_fortime,
                                  "转发的图片" + Db_forpicListStr,
                                  "转发的视频" + Db_forVideo + "当前页数" + str(nowPageNum))
                            wirtdeDb(Db_name, Db_id, Db_talktext, Db_picListStr, Db_Video, Db_time,
                                     Db_forTest, Db_forname,
                                     Db_forid, Db_fortime, Db_forpicListStr, Db_forVideo)
                        except:
                            print("数据" + "文字---" + Db_talktext, "姓名" + Db_name,
                                  "id" + Db_id, "时间" + Db_time,
                                  "图片" + Db_picListStr,
                                  "视频" + Db_Video + "当前页数" + str(nowPageNum))
                            wirtdeDb(Db_name, Db_id, Db_talktext, Db_picListStr, Db_Video, Db_time,
                                     "",
                                     "", "", "", "", "")


@async
def wirtdeDb(Db_name, Db_id, Db_talktext, Db_picListStr, Db_Video, Db_time, Db_forTest, Db_forname,
             Db_forid,
             Db_fortime, Db_forpicListStr, Db_forVideo):
    url = 'http://youyiku-yishu.cn/WebApp/WbBooks/getwbContent'

    # 数据进行Body拼接-
    body = '{"authorName":' + Db_name + ',"authorId":' + str(
        Db_id) + ',"timestamp":' + Db_time + ',"content":"' + Db_talktext + '","imageList":"' + Db_picListStr + '","videoList":"' + Db_Video + '","forcontent":"' + Db_forTest + '","forimageList":"' + Db_forpicListStr + '","forvideoList":"' + Db_forVideo + '"}'

    # 模拟请求头
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(url + body)
    # 这里发送了请求的同时也打印了想看的返回值
    print("返回参数----->" + requests.post(url, data={'value': body}, headers=headers).text)
