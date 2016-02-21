# -*- coding:utf-8 -*-
import os
import codecs

from model import *

#DIR="/home/xlore/server36/infobox/"
DIR="/Users/Miyayx/data"
ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE=os.path.join(DIR, "enwiki-template-baidu-attribute.dat")
ENWIKI_PROPERTY_TRANSLATED=os.path.join(DIR, "enwiki-propertyList-translated.dat")
ENWIKI_INFOBOX_VALUE_TRANSLATED=os.path.join(DIR, "enwiki-infobox-value-translated.dat")

#BAIDU_DIR = "/home/xlore/server36/baikedump/"
#BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")
#BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "baidu-instance-concept.dat")
#
#ENWIKI_DIR = "/home/xlore/disk2/raw.wiki/"
#ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "enwiki-infobox-new.dat")
#ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-category.dat")
#
#SEEDS=os.path.join(DIR, "enwiki-baidu-matched-property-2.dat")

#BAIDU_DIR = "/home/xlore/server36/infobox/small"
BAIDU_DIR = "/Users/Miyayx/data/small"
BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "small-baidu-title-property.dat")
BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "small-baidu-instance-concept.dat")

ENWIKI_DIR = "/Users/Miyayx/data/small"
ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "small-enwiki-infobox.dat")
ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "small-enwiki-category.dat")

SEEDS=os.path.join(ENWIKI_DIR, "small-enwiki-baidu-matched-property.dat")

#WIKI_CROSSLINGUAL = "/home/xlore/Xlore/etc/data/cross.lingual.links/cl.en.zh.all"
WIKI_CROSSLINGUAL = "/Users/Miyayx/data/cl.en.zh.all"
BAIDU_CROSSLINGUALL = ""


def read_baidu_properties(fn):
    d = {}
    for line in codecs.open(fn, 'r','utf-8'):
        try:
            title, info = line.strip('\n').split('\t')
        except:
            continue
        for item in info.split('::;'):
            try:
                p, v = item.split(':::')
            except:
                continue
            prop = d.get(p, Property(p))
            prop.articles.append(title)
            if len(v) > 0:
                prop.values.append(v)
            d[p] = prop
    return d

def read_wiki_properties(fn):
    """
    return:
        dict of Domain
    """
    print "Reading %s ..."%fn
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if not '\t\t' in line:
            continue
        title, info = line.strip('\n').split('\t\t')
        info = info.split('\t')[0]
        tem, infobox = info.split(':::::',1)
        tem = 'template:'+tem
        
        if not tem in d:
            d[tem] = Domain(tem)
        for pair in infobox.split('::::;'):
            p, v = pair.split('::::=')
            prop = d[tem].wiki_properties.get(p, Property(p))
            prop.articles.append(title)
            if len(v) > 0:
                prop.values.append(v)
            d[tem].wiki_properties[p] = prop
    return d

def read_wiki_infobox(fn):
    """
    d: key:template, value: instance set
    """
    print "Reading wiki infobox ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if not '\t\t' in line:
            continue
        title, info = line.strip('\n').split('\t\t')
        info = info.split('\t')[0]
        tem, infobox = info.split(':::::',1)
        tem = 'template:'+tem
        
        if not tem in d:
            d[tem] = set()
        d[tem].add(title)
    return d

def read_wiki_instance_concept(fn, a_set):
    print "Reading wiki instance and concept ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        article, categories = line.strip('\n').split('\t\t')
        if a_set: #如果有a_set，以a_set作为限制，减少读入的数据量，只记录在a_set中的article 
            if article in a_set:
                d[article] = set(categories.split(';'))
        else: #没有a_set，记录全部
            d[article] = set(categories.split(';'))
    return d

def read_baidu_concept_instance(fn):
    print "Reading baidu concepts and instances ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, categories = line.strip('\n').split('\t')
            for c in categories.split(';'):
                if not c in d:
                    d[c] = set()
                d[c].add(article)
        except:
            print 'Read Error:',line
    return d

def read_instance_property(fn):
    print "Reading baidu instance and property ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, facts = line.strip('\n').split('\t')
            d[article] = set([fact.split(':::')[0] for fact in facts.split('::;')])
        except:
            print line
    return d

def read_seeds(fn):
    print "Reading seeds..."
    #d = dict(line.strip('\n').rsplit('\t', 1) for line in codecs.open(fn, 'r', 'utf-8'))
    d = [tuple(line.strip('\n').rsplit('\t', 1)) for line in codecs.open(fn, 'r', 'utf-8')]
    return d

def read_crosslingual(fn):
    return dict((line.strip('\n').split('\t')) for line in codecs.open(fn, 'r', 'utf-8'))

def read_translate_result(fn):
    return read_crosslingual(fn)

    
if __name__ == '__main__':
    read_instance_property(BAIDU_INFOBOX)
