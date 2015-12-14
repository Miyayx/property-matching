# -*- coding:utf-8 -*-
from similarity import *

BAIDU_DIR = "/home/xlore/server36/baikedump/"
BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")
BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "baidu-instance-concept.dat")

ENWIKI_DIR = "/home/xlore/disk2/raw.wiki/"
ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "enwiki-infobox-new.dat")
ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-category.dat")

WIKI_CROSSLINGUAL = "/home/xlore/Xlore/etc/data/cross.lingual.links/cl.en.zh.all"
BAIDU_CROSSLINGUALL = ""

def read_wiki_infobox(fn):
    """
    d: key:template, value: instance set
    """
    d = {}
    for line in open(fn):
        if not '\t\t' in line:
            continue
        title, info = line.strip('\n').split('\t\t')
        info = info.split('\t')[0]
        if not title in matched_ins: #没有crosslingual的instance就不要了
            continue
        tem, infobox = info.split(':::::',1)
        tem = 'template:'+tem
        
        if not tem in d:
            d[tem] = set()
        d[tem].add(title)
    return d

def read_instance_concept(fn):
    d = {}
    for line in open(fn):
        article, categories = line.strip('\n').split('\t\t')
        d[article] = set(categories.split(';'))
    return d

def replace_enconcepts(tem_con, *clfns):
    cl = {}
    for fn in clfns:
        for line in open(fn):
            a, b = line.strip('\n').split('\t')
            cl[a] = b

    d = {}
    for tem, cons in tem_con.iteritems():
        d[tem] = set([cl[con] for con in cons if con in cl])
    return d

def read_concept_instance(fn):
    d = {}
    for line in open(fn):
        article, categories = line.strip('\n').split('\t\t')
        for c in categories.split(';'):
            d[c] = d.get(c,[]) + [article]
    return d

def read_instance_property(fn):
    d = {}
    for line in open(fn):
        article, facts = line.strip('\n').split('\t\t')
        d[article] = set([fact.split(':::')[0] for fact in facts.split('::;')])
    return d

def find_attribute_in_baidu():
    tem_ins = read_wiki_infobox(ENWIKI_INFOBOX)
    ins_con = read_instance_concept(ENWIKI_INSTANCE_CONCEPT)
    tem_con = {}
    for tem, inses in tem.iteritems():
        tem_con[tem] = set()
        for ins in ines:
            tem_con[tem] = tem_con[tem].union(ins_con[ins])
    del tem_ins, ins_con

    tem_zhcon = replace_enconcepts(tem_con, WIKI_CROSSLINGUAL)
    del tem_con
    zh_con_ins = read_concept_instance(BAIDU_INSTANCE_CONCEPT)
    tem_zhins = {}
    for tem, cons in tem_zhcon.iteritems():
        tem_zhins[tem] = set()
        for con in cons:
            tem_zhins[tem] = tem_zhins[tem].union(zh_con_ins[con])
    del zh_con_ins
    zh_ins_attr = read_instance_property(BAIDU_INFOBOX)
    tem_baidu_attr = {}
    for tem, inses in zh_ins_attr.iteritems():
        tem_baidu_attr[tem] = set()
        tem_baidu_attr[tem] = tem_baidu_attr[tem].union(zh_ins_attr[tem])

    for tem, attrs in tem_baidu_attr.iteritems():
        print tem, len(attrs)

