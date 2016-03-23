# -*- coding:utf-8 -*-
import codecs

def read_inherit_template(fn):
    tems = [line.strip('\n') for line in codecs.open(fn)]

def read_template_triple(fn):
    print "Reading %s ..."%fn
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        tem, tl, rl = line.strip('\n').split('\t')[:3]
        if not tem in d:
            d[tem] = {}
        d[tem][tl] = rl

    return d

def read_redirect_template(fn):
    print "Reading %s ..."%fn
    return dict(line.strip('\n').split('\t') for line in codecs.open(fn, 'r', 'utf-8'))

def read_wiki_infobox(fn):
    print "Reading %s ..."%fn
    a_tem = {}
    a_infobox = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if not '\t\t' in line:
            continue
        title, info = line.strip('\n').split('\t\t')
        info = info.split('\t')[0]
        tem, infobox = info.split(':::::',1)
        tem = 'Template:'+tem

        a_tem[title] = tem
        
        for pair in infobox.split('::::;'):
            try:
                p, v = pair.split('::::=')
            except:
                print title, tem, pair
                continue
            if not title in a_infobox:
                a_infobox[title] = {}
            else:
                a_infobox[title][p] = v
    return a_tem, a_infobox
