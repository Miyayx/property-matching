# -*- coding:utf-8 -*-
import os
import codecs

from similarity import *
from fileio import *

def compare(p1, p2):
    """
    对比两个property
    1. label edit distance
    2. 不同时出现在同一个文章
    3. value 对比: 文本，数字，日期
    """
    #similarities = [label_similarity, valuesimilarity_number, valuesimilarity_date, range_similarity]
    similarities = [label_similarity, valuesimilarity_number, valuesimilarity_date, reversed_article_similarity]
    print "Compare:",p1.label, p2.label
    result = []
    for fun in similarities:
        r = fun(p1, p2)
        print fun.__name__, r
        result.append(r)
        
    #print "label:", edit_distance_similarity(p1.label, p2.label)
    #print "reversed_articel_similarity", reversed_article_similarity(p1, p2)
    #print "valuesimilarity_number", valuesimilarity_number(p1, p2)
    #print "valuesimilarity_date", valuesimilarity_date(p1, p2)
    #print "valuesimilarity_literal", valuesimilarity_literal(p1, p2)
    return sum(result)

def merge_baidu_synonym(domain_dict):

    for tem, domain in domain_dict.items():
        bps = domain_dict.baidu_properties.values()
        cluster = {}
        cluster2 = {}
        for bp1 in bps:
            for bp2 in bps:
                if bp1 == bp2:
                    continue
                c = compare(bp1, bp2)
                # 还差合并的代码


def main():
    
    d = read_baidu_properties(BAIDU_INFOBOX)
    #for line in codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'r', 'utf-8'):
    #    try:
    #        tem, attributes = line.strip('\n').split('\t',1)
    #        if not tem == 'template:infobox book':
    #            continue
    #        attrs = attributes.strip(':::').split(':::')
    #        print "Template:", tem, len(attrs)
    #        for i in range(len(attrs)):
    #            Max = (None, 0)
    #            if not attrs[i] in d:
    #                continue
    #            p1 = d[attrs[i]]
    #            for j in range(i+1, len(attrs)):
    #                #print attrs[i], attrs[j], compare(d[attrs[i]], d[attrs[j]])
    #                if attrs[i] in d and attrs[j] in d:
    #                    p2 = d[attrs[j]]
    #                    ras = reversed_article_similarity(p1, p2)
    #                    #print "RAS:",p1.label, p2.label, ras
    #                    if ras < 10000:
    #                        c = compare(p1, p2)
    #                        if c > Max[1]:
    #                            Max = (p2, c)
    #            if not Max[0] == None:
    #                print "Most similar:", p1.label, Max[0].label, Max[1] 
    #    except:
    #        print line
        
    print compare(d[u'五笔(86&98)'], d[u'五笔86&98'])
    #print compare(d[u'英文名'], d[u'外文名'])
    #print compare(d[u'其它外文名'], d[u'外文名'])

if __name__ == '__main__':
    main()
    
