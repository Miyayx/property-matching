# -*- coding:utf-8 -*-
from similarity import *

import os
import codecs
from sklearn.feature_extraction.text import TfidfTransformer

from fileio import *
from model import *

"""
找到enwiki Template领域下，baidu中涉及的article
"""

def generate_domain_articles():
    tem_domain = read_wiki_properties(ENWIKI_INFOBOX)
    tem_ins = read_wiki_template_instance(ENWIKI_INFOBOX)
    tem_ins_infobox = read_wiki_infobox(ENWIKI_INFOBOX)
    inses = []
    
    #所有wiki instance
    for domain in tem_domain.itervalues():
        for prop in domain.wiki_properties.values():
            inses += prop.articles

    #计算wiki property在特定domain下的常用程度
    for tem, domain in tem_domain.iteritems():
        for prop in domain.wiki_properties.values():
            prop.popular = len(prop.articles)*0.1/len(tem_ins[tem])

    #加入翻译结果
    add_translate_labels(tem_domain)
    add_translate_values(tem_domain)

    # tem涉及到的concept
    ins_con = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT, set(inses))
    del inses
    tem_con = {}
    print "tem_con"
    for tem, inses in tem_ins.iteritems():
        s = []
        for ins in inses:
            s += ins_con[ins]
        tem_con[tem] = set(s)
    del tem_ins, ins_con

    # template涉及到的baidu instance
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

    zh_ins_infobox = read_infobox(BAIDU_INFOBOX)
    tem_zhins_infobox = {}
    for tem, inses in tem_zhins.iteritems():
        ad = ArticleDomain(tem)
        for ins in inses:
            if ins in zh_ins_attr:
                article = Article(ins)
                for p, v in zh_ins_attr[ins].iteritems():
                    prop = Property(p)
                    prop.value = v
                    article.infobox[p] = prop
                ad.articles[ins]=article
        tem_zhins_infobox[tem] = ad
            
    #计算baidu property在特定domain下的常用程度
    #for tem, domain in tem_domain.iteritems():
    #    for prop in domain.baidu_properties.values():
    #        prop.popular = len(prop.articles)*0.1/len(tem_zhins[tem])

    return tem_ins_infobox, tem_zhins_infobox
    
