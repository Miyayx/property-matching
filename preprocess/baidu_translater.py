#-*- coding:utf-8 -*-

import urllib
import json
import sys,os,re

from utils import *
import configs

class Translater:
    BAIDU_API_KEY=configs.BAIDU_API_KEY
    API_URL=("http://openapi.baidu.com/public/2.0/bmt/translate?client_id=" + BAIDU_API_KEY + "&q=%s&from=%s&to=%s")

    def __init__(self):
        pass

    def translate(self, s, source_lan="en", target_lan="zh"):
        URL = "http://openapi.baidu.com/public/2.0/bmt/translate?client_id=%s&from=%s&to=%s&q="%(Translater.BAIDU_API_KEY, source_lan, target_lan)
        j = urllib.urlopen((URL+s).encode("UTF-8")).read()
        #print j
        return self.parse_json(j)

    def parse_json(self, j):
        d = {}
        Json = json.loads(j)
        if not 'trans_result' in Json:
            return d
        for item in Json['trans_result']:
            src, dst = item['src'], item['dst']
            d[src] = dst
        return d

