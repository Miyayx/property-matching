#-*- coding:utf-8 -*-

import codecs
import sys,os
import re

from difflib import SequenceMatcher

ZHWIKI_INFOBOX="/home/xlore/server36/infobox/zhwiki-infobox-new.dat"
BAIDU_INFOBOX ="/home/xlore/server36/baikedump/baidu-title-property.dat"
ZHWIKI_BAIDU_ALIGNMENT="/home/xlore/server36/infobox/zhwiki-baidu-matched-property.dat"

"""
通过对齐的zhwiki与baidu的article，找出同一个article中对齐的property
"""

def similar(a, b):
    seta = set(re.findall(r'\d+', a))
    print seta
    setb = set(re.findall(r'\d+', b))
    print setb
    if len(seta) > 0 or len(setb) > 0:
        return len(seta&setb)*1.0 / len(seta|setb)
    return SequenceMatcher(None, a, b).ratio()

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
                    if len(fact.split('::::=')) < 2:
                        continue
                    k, v = fact.split('::::=')
                    d[article][tem][k] = v
    return d

def find_aligned_attributes(baidufn, fo, zhwiki):
    d = {}
    fw = codecs.open(fo, 'w', 'utf-8')
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
                        if not tem in d:
                            d[tem] = {}
                        align = None
                        cans = {}
                        for k1, v1 in infos.iteritems():
                            if k == k1:
                                if not k1 in d[tem]:
                                    d[tem][k1] = {}
                                d[tem][k1][k] = d[tem][k1].get(k, 0.0)+1.0
                                align = '%s\t%s\t%s\t%s\t%s'%(tem,k1,k,v1,v)
                                break
                            else:
                                s = similar(v, v1)
                                if s >= 0.4:
                                    cans['%s\t%s\t%s\t%s\t%s'%(tem,k1,k,v1,v)] = s
                                    #print tem, k1, k, v1, v, s
                                    if not k1 in d[tem]:
                                        d[tem][k1] = {}
                                    #d[tem][k1].add(k)
                                    d[tem][k1][k] = d[tem][k1].get(k, 0.0)+s
                        if align:
                           #print align
                           pass
                        elif cans:
                           #text, s = sorted(cans.items(), key=lambda x:x[1])[0]
                           #print text, s
                           pass
                except Exception,e:
                    print e
                    print 'Error:',fact
    print 'Template Number:', len(d)
    attr_num = 0
    for attrs in d.values():
       attr_num += len(attrs)
    print 'Total aligned attrs:', attr_num
    for tem, attrs in d.iteritems():
        for zh, bai in attrs.iteritems():
            for a, s in sorted(bai.iteritems(), key=lambda x:x[1], reverse=True):
                #print tem, zh, a, s
                avg_s = s*1.0/len(bai)
                if avg_s < 0.4:
                    continue
                fw.write("%s\t%s\t%s\t%f\n"%(tem, zh, a, avg_s))
                fw.flush()
    fw.close()

if __name__=='__main__':
    zhwiki = read_wiki_infobox(ZHWIKI_INFOBOX)
    find_aligned_attributes(BAIDU_INFOBOX, ZHWIKI_BAIDU_ALIGNMENT,  zhwiki)

