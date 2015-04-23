#!/usr/bin/python
# -*- coding:utf-8 -*-

import re, math
from collections import Counter


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text, lan):
    WORD = re.compile(r'.')
    if 'en' == lan:
        WORD = re.compile(r'\w+')
    words = WORD.findall(text)
    #print words
    #words = text 
    return Counter(words)

def has_chinese(text):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(text.decode('utf-8'))
    return True if match else False

def only_chinese(text):
    enPattern = re.compile(u'\w+')
    match = enPattern.search(text.decode('utf-8'))
    return False if match else True

import config
import urllib2
import json
def translate_en2zh(text):
    url = 'http://openapi.baidu.com/public/2.0/bmt/translate?client_id=%s&q=%s&from=en&to=zh'%(config.baidu_id, text)
    try:
        res = urllib2.urlopen(url).read()
        j = json.loads(res)
        return j['trans_result'][0]['dst'].encode('utf-8')
    except:
        return text

