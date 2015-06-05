# -*- coding:utf-8 -*-
"""
本模块程序负责：
    1. 根据给的template label与对应中英文，将template label替换成对应的display label 
    2. 根据给的中英文对照表，将match的中英文property合并
"""
import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl4")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl4")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl5")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl5")

DIR2 = "/home/xlore/XloreData/etc/ttl/"
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR2, "zhwiki-template-triple.dat") 
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR2, "enwiki-template-triple.dat") 

def read_template_label(fn):
    labels = {}
    for line in codecs.open(fn,'r','utf-8'):
        k,v = line.split('\t')[:2]
        k = k[0:k.index('(')]
        if k in labels:
            print k
        labels[k] = v
    return labels

def read_and_write(fn, ofn, en_labels, zh_labels ):
    re_count = 0 
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                l = line[line.index('"')+1: line.rindex('"')]
                if "@en" in line:
                    if l in en_labels:
                        re_count += 1
                        line = line.replace(l, en_labels[l])
                if "@zh" in line:
                    if l in zh_labels:
                        re_count += 1
                        line = line.replace(l, zh_labels[l])
            fw.write(line)
            fw.flush()
    fw.close()
    print "Replace num:%d"%(re_count)

