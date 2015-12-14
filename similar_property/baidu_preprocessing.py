# -*- coding:utf-8 -*-
import os

from similarity import *

BAIDU_DIR = "/home/keg/data/baikedump/"
INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")

class Property:
    def __init__(self, l):
        self.label = l
        self.articles = []
        self.values = []

def read_properties(fn):
    d = {}
    for line in open(fn):
        title, info = line.strip('\n').split('\t')
        for item in info.split('::;'):
            try:
                p, v = item.split(':::')
            except:
                continue
            prop = d.get(p, Property(p))
            prop.articles.append(title)
            prop.values.append(v)
            d[p] = prop
    return d

def compare(p1, p2):
    """
    对比两个property
    1. label edit distance
    2. 不同时出现在同一个文章
    3. value 对比: 文本，数字，日期
    """
    print "Compare:",p1.label, p2.label
    print "label:", edit_distance_similarity(p1.label, p2.label)
    print "reversed_articel_similarity", reversed_article_similarity(p1, p2)
    print "valuesimilarity_number", valuesimilarity_number(p1, p2)
    print "valuesimilarity_date", valuesimilarity_date(p1, p2)
    #print "valuesimilarity_literal", valuesimilarity_literal(p1, p2)

def main():
    
    d = read_properties(INFOBOX)
    compare(d['英文名'], d['中文名'])
    compare(d['英文名'], d['外文名'])
    compare(d['其它外文名'], d['外文名'])

if __name__ == '__main__':
    main()
    



