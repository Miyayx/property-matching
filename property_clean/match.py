# -*- coding:utf-8 -*-
"""
本模块程序负责：
    1. 根据给的template label与对应中英文，将template label替换成对应的display label 
    2. 根据给的中英文对照表，将match的中英文property合并
"""
import re
import os
import codecs

from prop_io import *

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl4")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl4")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl5")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl5")

DIR2 = "/home/xlore/XloreData/etc/ttl/"
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR2, "zhwiki-template-triple.dat") 
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR2, "enwiki-template-triple.dat") 

def read_template_label(fn):
    """
    Returns:
        k: template label v:display label
    """
    labels = {}
    for line in codecs.open(fn,'r','utf-8'):
        k,v = line.split('\t')[:2]
        k = k[0:k.index('(')]
        if k in labels:
            print k
        labels[k] = v
    return labels

def merge_by_template_label():
    zh_temp_label = read_template_label(ZHWIKI_TEMPLATE_LABEL)
    en_temp_label = read_template_label(ENWIKI_TEMPLATE_LABEL)
    label_uri = read_label_uri(PROPERTY_LIST_TTL)
    uri_labels = read_uri_labels(PROPERTY_LIST_TTL)
    for tl, dl in zh_temp_label.items():
        if tl in label_uri:
            u = label_uri[tl]
        uri_labels[uri]['zh'] = dl
    for tl, dl in en_temp_label.items():
        if tl in label_uri:
            u = label_uri[tl]
        uri_labels[uri]['en'] = dl
    write_new_property_list(O_PROPERTY_LIST_TTL, uri_labels)

def merge_by_matched_pair():
    pass

if __name__ == "__main__":
    merge_by_template_label()

