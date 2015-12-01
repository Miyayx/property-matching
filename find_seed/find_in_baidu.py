# -*- coding:utf-8 -*-
import os

"""
通过已有的wikipedia matched properties 从百度中找到对应的property
"""

BAIKE_DIR = "/home/keg/data/baikedump"
BAIDU_PROPERTY = os.path.join(BAIKE_DIR, "baidu-propertyList-all.dat")
DIR = "/home/keg/data/infobox"
MATCHED_TEMPLATE_LABEL_ALL = os.path.join(DIR, "matched-template-label-all.dat")
BAIDU_MATCHED_PROPERTY = os.path.join(DIR, "baidu-matched-property.dat")

def clean_label(label):
    if '[[' in label:
        label = label[2:-2]
        label = label.split('|')[0]
    return label

def find_in_baidu():
    fw = open(BAIDU_MATCHED_PROPERTY, 'w')
    wiki_zh_en = {}
    for line in open(MATCHED_TEMPLATE_LABEL_ALL):
        en, zh = line.strip('\n').split('\t')
        en = clean_label(en)
        zh = clean_label(zh)
        wiki_zh_en[zh] = en
        
    #wiki_zh_en = dict((list(reversed(line.strip('\n').split('\t')))) for line in open(MATCHED_TEMPLATE_LABEL_ALL))
    baidu_zh = [line.strip('\n') for line in open(BAIDU_PROPERTY)]
    for p in baidu_zh:
        if p in wiki_zh_en:
            fw.write(p+'\t'+wiki_zh_en[p]+'\n')
    fw.close()

if __name__ == "__main__":
    find_in_baidu()

        
