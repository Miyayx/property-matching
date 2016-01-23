#-*- coding:utf-8 -*-

import codecs
import sys,os

from difflib import SequenceMatcher

ZHWIKI_INFOBOX="/home/xlore/server36/infobox/zhwiki-infobox-new.dat"
BAIDU_INFOBOX="/home/xlore/server36/baikedump/baidu-title-property.dat"

"""
通过对齐的zhwiki与baidu的article，找出同一个article中对齐的property
"""

def similar(a, b):
    return SequenceMatcher(a, b).ratio()

def read_wiki_infobox(fn):
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if len(line.split('\t\t')) < 2:
            continue
        else:
            article, infos = line.strip('\n').split('\t\t')
            d[article] = {}
            new_infos = []
            for info in infos.split('\t'): #对每个template new_facts = {}
                tem, facts = info.split(':::::', 1)
                d[article][tem] = {}
                for fact in facts.split('::::;'):
                    k, v = fact.split('::::=')
                    d[article][tem][k] = v
    return d

def find_aligned_attributes(baidufn, zhwiki):
    for line in codecs.open(baidufn, 'r', 'utf-8'):
        if len(line.split('\t')) < 2:
            continue
        else:
            article, facts = line.strip('\n').split('\t')
            if not article in zhwiki: #该文章在zhwiki里没有，跳过
                continue
            for fact in facts.split('::;'):
                if len(fact.split(':::')) < 2:
                    continue
                try:
                    k, v = fact.split(':::')
                    for tem, infos in zhwiki[article].iteritems():
                        for k1, v1 in infos.iteritems():
                            if k == k1:
                                print tem,k,k1,v,v1
                                break
                            elif similar(v, v1) > 0.6:
                                print tem, k, k1, v, v1
                except:
                    print 'Error:',fact

if __name__=='__main__':
    zhwiki = read_wiki_infobox(ZHWIKI_INFOBOX)
    find_aligned_attributes(BAIDU_INFOBOX, zhwiki)


