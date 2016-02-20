#-*- coding:utf-8 -*-

import os
import codecs

BAIDU_DIR = "/home/xlore/server36/baikedump/"
BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")
BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "baidu-instance-concept.dat")
BAIDU_PROPERTY_CONCEPT=os.path.join(BAIDU_DIR, "baidu-property-concept.dat")

ENWIKI_DIR = "/home/xlore/disk2/raw.wiki/"
ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "enwiki-infobox-new.dat")
ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-category.dat")
ENWIKI_PROPERTY_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-property-concept.dat")
ENWIKI_SMALL_PROPERTY_CONCEPT=os.path.join(ENWIKI_DIR, "small-enwiki-property-concept.dat")

def read_wiki_infobox(fn):
    """
    d: key:template, value: instance set
    """
    print "Reading wiki infobox ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if not '\t\t' in line:
            continue
        try:
            title, info = line.strip('\n').split('\t\t')
            info = info.split('\t')[0]
            tem, infobox = info.split(':::::',1)
            tem = 'template:'+tem
            
            if not tem in d:
                d[tem] = {}
            for fact in info.split('::::;'):
                k, v = fact.split('::::=')
                if not k in d[tem]:
                    d[tem][k] = set()
                d[tem][k].add(title)
        except Exception,e:
            print e
            print line
    return d

def read_baidu_infobox(fn):
    print "Reading baidu instance and property ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, facts = line.strip('\n').split('\t')
            d[article] = set([fact.split(':::')[0] for fact in facts.split('::;')])
        except:
            print line
    return d

def read_wiki_instance_concept(fn):
    print "Reading wiki instance and concept ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        article, categories = line.strip('\n').split('\t\t')
        d[article] = set(categories.split(';'))
    return d

def read_baidu_instance_concept(fn):
    print "Reading baidu concepts and instances ..."
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            article, categories = line.strip('\n').split('\t')
            d[article] = set(categories.split(';'))
        except:
            print 'Read Error:',line
    return d

if __name__=="__main__":
    templates = ('template:infobox film', 'template:infobox television', 'template:infobox company')
    d = read_wiki_infobox(ENWIKI_INFOBOX)
    ins_con = read_wiki_instance_concept(ENWIKI_INSTANCE_CONCEPT)
    prop_con = {}
    for tem, prop_ins in d.iteritems():
        for p, inses in prop_ins.iteritems():
            k = tem+':::'+p
            for i in inses:
                if not k in prop_con:
                    prop_con[k] = set()
                for c in ins_con[i]:
                    prop_con[k].add(c)

    small_prop_con = {}
    for tem, prop_ins in d.iteritems():
        if not tem in templates:
            continue
        for p, inses in prop_ins.iteritems():
            k = tem+':::'+p
            for i in inses:
                if not k in small_prop_con:
                    small_prop_con[k] = set()
                for c in ins_con[i]:
                    small_prop_con[k].add(c)
            
    fw = codecs.open(ENWIKI_PROPERTY_CONCEPT, 'w', 'utf-8')
    for p, cons in prop_con.iteritems():
        fw.write("%s\t%s\n"%(p, ';'.join(cons)))
    fw.close()

    fw2 = codecs.open(ENWIKI_SMALL_PROPERTY_CONCEPT, 'w', 'utf-8')
    for p, cons in small_prop_con.iteritems():
        fw2.write("%s\t%s\n"%(p, ';'.join(cons)))
    fw2.close()

    del d
    del ins_con

    d = read_baidu_infobox(BAIDU_INFOBOX)
    ins_con = read_baidu_instance_concept(BAIDU_INSTANCE_CONCEPT)
    prop_con = {}
    for ins, props in d.iteritems():
        for p in props:
            if not p in prop_con:
                prop_con[p] = set()
            for c in ins_con.get(ins, []):
                prop_con[p].add(c)

    fw = codecs.open(BAIDU_PROPERTY_CONCEPT, 'w', 'utf-8')
    for p, cons in prop_con.iteritems():
        fw.write("%s\t%s\n"%(p, ';'.join(cons)))
    fw.close()
    
    
