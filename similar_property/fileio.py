# -*- coding:utf-8 -*-
import os
import codecs

from model import *

#DIR="/home/xlore/server36/infobox/"
#DIR="/Users/Miyayx/data"
DIR = "/data/xlore20160223/Template/"
ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE=os.path.join(DIR, "enwiki-template-baidu-attribute.dat")
ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE_NUMBER=os.path.join(DIR, "enwiki-template-baidu-attribute-number.dat")
#ENWIKI_PROPERTY_TRANSLATED=os.path.join(DIR+"translate", "enwiki-propertyList-translated.dat")
ENWIKI_PROPERTY_TRANSLATED=os.path.join(DIR+"translate", "enwiki-property-label-translated.dat")
ENWIKI_INFOBOX_VALUE_TRANSLATED=os.path.join(DIR+"translate", "enwiki-infobox-value-translated.dat")

#BAIDU_DIR = "/home/xlore/server36/baikedump/"
BAIDU_DIR = "/data/baidu/"
BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")
BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "baidu-instance-concept.dat")

#ENWIKI_DIR = "/home/xlore/disk2/raw.wiki/"
ENWIKI_DIR = "/data/xlore20160223/wikiExtractResult/"
ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "enwiki-infobox-tmp-infobox-replaced.dat")
ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-category.dat")

SEEDS=os.path.join(DIR, "enwiki-baidu-matched-property-all.dat")

#BAIDU_DIR = "/home/xlore/server36/infobox/small"
#BAIDU_DIR = "/Users/Miyayx/data/small"
#BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "small-baidu-title-property.dat")
#BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "small-baidu-instance-concept.dat")

#ENWIKI_DIR = "/Users/Miyayx/data/small"
#ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "small-enwiki-infobox.dat")
#ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "small-enwiki-category.dat")
#
#SEEDS=os.path.join(ENWIKI_DIR, "small-enwiki-baidu-matched-property.dat")

#WIKI_CROSSLINGUAL = "/home/xlore/Xlore/etc/data/cross.lingual.links/cl.en.zh.all"
#WIKI_CROSSLINGUAL = "/Users/Miyayx/data/cl.en.zh.all"
#WIKI_CROSSLINGUAL = "/data/xlore20160223/Template/cl.en.zh.all"
WIKI_CROSSLINGUAL = "/home/xlore/Xlore/etc/data/cross.lingual.links/cl.en.zh.all"
#WIKI_CROSSLINGUAL = "/Users/Miyayx/data/cl.en.zh.all"
BAIDU_CROSSLINGUALL = ""

def clean_baidu_label(label):
    return label.strip().replace(" ","").replace(" ","").replace("\t","").replace(u'\u200b','').replace(u'\u3000','')

def read_baidu_properties(fn):
    print "Reading %s ..."%fn
    d = {}
    for line in codecs.open(fn, 'r','utf-8'):
        try:
            title, info = line.strip('\n').split('\t')
        except:
            continue
        for item in info.split('::;'):
            try:
                p, v = item.split(':::')
                p = clean_baidu_label(p)
            except:
                continue
            prop = d.get(p, Property(p))
            #prop.articles.append(title)
            #if len(v) > 0:
            #    prop.values.append(v)
            if len(v) > 0:
                prop.infobox[title] = v
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
        if not tem.lower().startswith('template'):
            tem = 'template:'+tem
        
        if not tem in d:
            d[tem] = Domain(tem)
        for pair in infobox.split('::::;'):
            try:
                p, v = pair.split('::::=')
                prop = d[tem].wiki_properties.get(p, Property(p))
                #prop.articles.append(title)
                #if len(v) > 0:
                #    prop.values.append(v)
                if len(v) > 0:
                    prop.infobox[title] = v
                d[tem].wiki_properties[p] = prop
            except:
                print infobox
    return d

def read_wiki_template_instance(fn):
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
        if not tem.lower().startswith('template'):
            tem = 'template:'+tem
        
        if not tem in d:
            d[tem] = set()
        d[tem].add(title)
    return d

def read_wiki_infobox(fn):
    print "Reading %s ..."%fn
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if not '\t\t' in line:
            continue
        title, info = line.strip('\n').split('\t\t')
        info = info.split('\t')[0]
        tem, infobox = info.split(':::::',1)
        if not tem.lower().startswith('template'):
            tem = 'template:'+tem
        
        ad = d.get(tem, ArticleDomain(tem))
        article = Article(title)

        for pair in infobox.split('::::;'):
            try:
                p, v = pair.split('::::=')
                if len(v) > 0:
                    prop = ArticleProperty(p)
                    prop.value = v
                    article.infobox[p] = prop
            except:
                print infobox
        ad.articles[title] = article
        d[tem] = ad
    return d

def read_baidu_infobox(fn):
    print "Reading baidu instance and property ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, facts = line.strip('\n').split('\t')
            d[article] = {}
            for fact in facts.split('::;'):
                p, v = fact.split(':::')
                p = clearn_baidu_label(p)
                if len(v) > 0:
                    d[article][p] = v
        except:
            print line
    return d

def read_wiki_instance_concept(fn, a_set):
    print "Reading wiki instance and concept ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, categories = line.strip('\n').split('\t\t')
            if a_set: #如果有a_set，以a_set作为限制，减少读入的数据量，只记录在a_set中的article 
                if article in a_set:
                    d[article] = set(categories.split(';'))
            else: #没有a_set，记录全部
                d[article] = set(categories.split(';'))
        except Exception,e:
            #print e
            #print line
            pass
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
            d[article] = set([clean_baidu_label(fact.split(':::')[0]) for fact in facts.split('::;')])
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
