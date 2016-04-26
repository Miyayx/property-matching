# -*- coding:utf-8 -*-
from similarity import *

import os
import codecs
from sklearn.feature_extraction.text import TfidfTransformer

from fileio import *
from model import *

"""
找到enwiki Template领域下，baidu中涉及的property
"""

def replace_by_crosslingual(tem_con, *clfns):
    cl = {}
    for fn in clfns:
        for line in codecs.open(fn, 'r','utf-8'):
            a, b = line.strip('\n').split('\t')
            cl[a] = b

    d = {}
    for tem, cons in tem_con.iteritems():
        d[tem] = set([cl[con] for con in cons if con in cl])
    return d

def add_translate_labels(tem_domain):
    """
    添加翻译的zhlable给property
    """
    tran = read_translate_result(ENWIKI_PROPERTY_TRANSLATED)
    for tem, domain in tem_domain.iteritems():
        for p, prop in domain.wiki_properties.iteritems():
            prop.zhlabel = tran.get(prop.label, "")

def add_translate_values(tem_domain):
    """
    添加翻译的zhvalue给property
    """
    tran = read_translate_result(ENWIKI_INFOBOX_VALUE_TRANSLATED)
    for tem, domain in tem_domain.iteritems():
        for p, prop in domain.wiki_properties.iteritems():
            prop.zhvalues = [tran.get(v, v) for v in prop.values]

def add_popular_wiki(tem_domain, tem_ins):
    if not tem_ins:
        tem_ins = read_wiki_template_instance(ENWIKI_INFOBOX)
    #计算wiki property在特定domain下的常用程度
    for tem, domain in tem_domain.iteritems():
        for prop in domain.wiki_properties.values():
            #prop.popular = len(prop.articles)*0.1/len(tem_ins[tem])
            prop.popular = len(prop.infobox.keys())*0.1/len(tem_ins[tem])

def add_popular_baidu(tem_domain, tem_zhins):
    #计算baidu property在特定domain下的常用程度
    for tem, domain in tem_domain.iteritems():
        for prop in domain.baidu_properties.values():
            #prop.popular = len(prop.articles)*0.1/len(tem_zhins[tem])
            prop.popular = len(prop.infobox.keys())*0.1/len(tem_zhins[tem])


def tfidf_filter(tem_attrs_count, tem_zhins):
    """
    self-define
    """
    attr_count = {}
    #for t, ats in tem_attrs_count.iteritems():
    #    for a, c in ats.iteritems():
    #        attr_count[a] = attr_count.get(a, 0)+c
        
    for t, attrs in tem_attrs_count.iteritems():
        total = sum(attrs.values())
        for a in attrs:
            #tf = attrs[a] * 1.0/attr_count[a]
            #tf = attrs[a] * 1.0/total
            tf = attrs[a] * 1.0/len(tem_zhins[t])
            if tf > 0.3:
                print t,a,tf
            #idf = -math.log(sum([1 for c in cons if p in c.properties])*1.0/len(cons))
            idf = math.log(len(tem_attrs_count)/(0.1+sum([1 for t in tem_attrs_count if a in tem_attrs_count[t]])*1.0))
            #print t, a, tf*idf

def tfidf_filter2(tem_attrs_count):
    """
    use scikit-learn
    """
    new_tem_attrs = {}
    new_tem_attrs_tfidf = {}

    tems = tem_attrs_count.keys()
    print "Templates:", len(tems)
    attrs = []
    for t, a_s in tem_attrs_count.iteritems():
        attrs.extend(a_s.keys())
    attrs = list(set(attrs))
    print "Attributes:", len(attrs)
    count = []
    for t in tems:
        l = [tem_attrs_count[t][a] if a in tem_attrs_count[t] else 0 for a in attrs ]
        count.append(l)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(count)
    tfidf = tfidf.toarray()
    f = codecs.open('attributes_by_con.dat', 'w', 'utf-8')
    for i in range(len(tems)):
        a_tfidf = {}
        for j in range(len(attrs)):
            if tfidf[i][j] > 0:
                a_tfidf[attrs[j]] = tfidf[i][j]
        for a, t in sorted(a_tfidf.iteritems(), key=lambda x:x[1], reverse=True)[:]:
            #print tems[i], a, t 
            if not tems[i] in new_tem_attrs:
                new_tem_attrs[tems[i]] = []
                new_tem_attrs_tfidf[tems[i]] = {}
            new_tem_attrs[tems[i]].append(a)
            new_tem_attrs_tfidf[tems[i]][a] = t
            f.write('%s %s %f\n'%(tems[i], a, t))
    f.close()
    return new_tem_attrs_tfidf

def domain_constrain_baidu(tem_domain, tem_zhins):
    import copy
    for tem, domain in tem_domain.iteritems():
        if not tem in tem_zhins:
            continue
        for attr, prop in domain.baidu_properties.iteritems():
            infobox = copy.copy(prop.infobox)
            for article, value in infobox.iteritems():
                if not article in tem_zhins[tem]:
                    #print 'Delete article ', article, 'from ', tem
                    prop.infobox.pop(article)

def generate_domain_properties():
    tem_domain = read_wiki_properties(ENWIKI_INFOBOX)
    tem_baiduattr_count, tem_ins, tem_zhins = find_attribute_in_baidu()

    #加入wiki popular信息
    add_popular_wiki(tem_domain, tem_ins)

    #加入翻译结果
    add_translate_labels(tem_domain)
    add_translate_values(tem_domain)

    ##### 算法
    #tfidf_filter(tem_baiduattr_count, tem_zhins)
    #tem_baiduattr = tfidf_filter2(tem_baiduattr_count)
    tem_baiduattr = tem_baiduattr_count
    #####

    baidu_properties = read_baidu_properties(BAIDU_INFOBOX)

    for tem, attrs in tem_baiduattr.items():
        if len(attrs) > 0:
            #for a in attrs.keys()[:100]:
            for a, v in sorted(attrs.iteritems(), key=lambda x: x[1], reverse=True)[:]:
                try:
                    tem_domain[tem].baidu_properties[a] = baidu_properties[a]
                except:
                    print 'Error Key',a

    domain_constrain_baidu(tem_domain, tem_zhins)

    #加入baidu popular信息
    add_popular_baidu(tem_domain, tem_zhins)

    return tem_domain
    
def find_attribute_in_baidu():
    """
    1. 找到使用template的instance
    2. 找到这些instance涉及的概念
    3. 通过已有的跨语言概念链接，找到baidu中对应的概念
    4. 通过概念下的instance， 找到概念下的attribute
    或者？？
    直接用跨语言instance？
    """
    tem_ins = read_wiki_template_instance(ENWIKI_INFOBOX)
    inses = []
    for ins in tem_ins.itervalues():
        inses += ins
    ins_con = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT, set(inses))
    del inses
    tem_con = {}
    print "tem_con"
    for tem, inses in tem_ins.iteritems():
        s = []
        for ins in inses:
            if ins in ins_con:
                s += ins_con[ins]
        tem_con[tem] = set(s)
    del ins_con

    tem_zhcon = replace_by_crosslingual(tem_con, WIKI_CROSSLINGUAL)
    del tem_con
    zh_con_ins = read_baidu_concept_instance(BAIDU_INSTANCE_CONCEPT)
    tem_zhins = {}
    print "tem_zhins"
    for tem, cons in tem_zhcon.iteritems():
        s = []
        for con in cons:
            if con in zh_con_ins:
                s += zh_con_ins[con]
        tem_zhins[tem] = set(s)
    del zh_con_ins
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c

    #count = 0
    #f = codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'w', 'utf-8')
    #print "Templates:",len(tem_baiduattr_count)
    #for tem, attrs in sorted(tem_baiduattr_count.items()):
    #    if len(attrs) > 0:
    #        print tem, len(attrs)
    #        f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
    #        f.flush()
    #        count += 1
    #f.close()
    #print "Templates which have attrs Count:",count
    return tem_baiduattr_count, tem_ins, tem_zhins

def find_attribute_in_baidu2():
    """
    1. 找到使用template的instance
    2. 找到这些instance涉及的概念
    3. 通过已有的跨语言概念链接，找到baidu中对应的概念
    4. 通过跨语言instance， 找到template下的attribute
    """
    tem_ins = read_wiki_template_instance(ENWIKI_INFOBOX)
    inses = []
    for ins in tem_ins.itervalues():
        inses += ins
    tem_zhins = replace_by_crosslingual(tem_ins, WIKI_CROSSLINGUAL)
    print "tem_zhins"
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c
    #tfidf_filter(tem_baiduattr_count, tem_zhins)
    tfidf_filter2(tem_baiduattr_count)

    #count = 0
    #f = codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE, 'w', 'utf-8')
    #print "Templates:",len(tem_baiduattr_count)
    #for tem, attrs in sorted(tem_baiduattr_count.items()):
    #    if len(attrs) > 0:
    #        print tem, len(attrs)
    #        f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
    #        f.flush()
    #        count += 1
    #f.close()
    #print "Templates which have attrs Count:",count

    return tem_baiduattr_count, tem_ins, tem_zhins

def find_attribute_in_baidu3():
    """
    1. 找到使用template的baidu instance
    2. 统计这些instance使用的property
    选出现频数站中间30%的property作为种子
    将使用种子集中超过60%的article
    3. 通过已有的跨语言概念链接，找到baidu中对应的概念
    4. 通过跨语言instance， 找到template下的attribute
    """
    tem_ins = read_wiki_template_instance(ENWIKI_INFOBOX)
    inses = []
    for tem, ins in tem_ins.iteritems():
        inses += ins

    tem_zhins = replace_by_crosslingual(tem_ins, WIKI_CROSSLINGUAL)
    print "tem_zhins"
    for tem, ins in tem_zhins.iteritems():
        print ','.join(ins)
    
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baiduattr_count = {}
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c

    #tfidf_filter(tem_baiduattr_count, tem_zhins)
    tfidf_filter2(tem_baiduattr_count)

    count = 0
    f = codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE+"3", 'w', 'utf-8')
    print "Templates:",len(tem_baiduattr_count)
    for tem, attrs in sorted(tem_baiduattr_count.items()):
        if len(attrs) > 0:
            print tem, len(attrs)
            f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
            f.flush()
            count += 1
    f.close()
    print "Templates which have attrs Count:",count

def find_attribute_in_baidu4():
    """
    1. 找到使用template的wiki instance
    2. 通过跨语言链接，找到Ie的对应Iz, Iz中的instance的property计数1(如果这个property在step4中又出现，则频数累加)
    3. 找到instance的Ce前10（以concept包含的instance数量排序）,且concept一定包含两个以上的instance
    4. 通过跨语言概念链接，找到baidu中对应的概念Cz, Cz下的instance(instance至少有两个概念在Cz中)的property计数1
    """
    tem_baiduattr_count = {}
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)

    # Step 1
    tem_enins = read_wiki_template_instance(ENWIKI_INFOBOX)

    # Step 2
    tem_zhins = replace_by_crosslingual(tem_enins, WIKI_CROSSLINGUAL)
    for tem, inses in tem_zhins.iteritems():
        a_c = {}
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c

    # Step 3 
    # get Ce
    from collections import Counter
    inses = []
    for tem, ins in tem_enins.iteritems():
        inses += ins
    ins_cons = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT, set(inses))
    del inses
    tem_con = {}
    for tem, inses in tem_enins.iteritems():
        cons = []
        for ins in inses:
            if ins in ins_cons:
                cons += ins_cons[ins]
        con_count = Counter(cons)
        tem_con[tem] = set([k for k, v in con_count.most_common() if v > 3][:10])
    del ins_cons

    # Step 4
    tem_zhcon = replace_by_crosslingual(tem_con, WIKI_CROSSLINGUAL)
    del tem_con
    zh_con_ins = read_baidu_concept_instance(BAIDU_INSTANCE_CONCEPT)
    tem_zhconins = {}
    for tem, cons in tem_zhcon.iteritems():
        s = []
        for con in cons:
            if con in zh_con_ins:
                s += zh_con_ins[con]
        tem_zhconins[tem] = set(s)
    del zh_con_ins
    for tem, inses in tem_zhconins.iteritems():
        a_c = tem_baiduattr_count[tem]
        for ins in inses:
            if ins in zh_ins_attr:
                for a in zh_ins_attr[ins]:
                    a_c[a] = a_c.get(a, 0)+1
        tem_baiduattr_count[tem] = a_c

    #tfidf_filter(tem_baiduattr_count, tem_zhins)
    tfidf_filter2(tem_baiduattr_count)

    count = 0
    f = codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE+"4-2", 'w', 'utf-8')
    print "Templates:",len(tem_baiduattr_count)
    for tem, attrs in sorted(tem_baiduattr_count.items()):
        if len(attrs) > 0:
            print tem, len(attrs)
            f.write(tem+'\t'+':::'.join(attrs.keys())+'\n')
            f.flush()
            count += 1
    f.close()
    print "Templates which have attrs Count:",count

if __name__ == "__main__":
    import time
    start = time.time()
    find_attribute_in_baidu4()
    print "Time Consuming:", time.time()-start

