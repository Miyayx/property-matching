#!/usr/bin/python
# -*- coding:utf-8 -*-

from models import *
from utils import *

import os

DIR = '/home/www/lmy_36mnt/data'

ENWIKI_DUMP_INFOBOX = os.path.join(DIR, 'wikiraw/enwiki-infobox-tmp.dat')
ZHWIKI_DUMP_INFOBOX = os.path.join(DIR, 'wikiraw/zhwiki-infobox-tmp.dat')
ENWIKI_CRAWL_INFOBOX = os.path.join(DIR, 'infobox/enwiki-infobox-scrapy.dat')
ZHWIKI_CRAWL_INFOBOX = os.path.join(DIR, 'infobox/zhwiki-infobox-scrapy.dat')

ZHWIKI_OUTPUT = os.path.join(DIR,'infobox/zhwiki-infobox-matched.dat')

def read_titles(fn):
    return [line.split('\t\t')[0] for line in open(fn)]

def label_filter(l):
    #return l.strip().strip('- ').lstrip('• ').strip('：')
    return l.decode('utf-8').strip(' ').lstrip(u'• ').strip(u'- ').strip(u'：').rstrip('*').strip(' ').encode('utf-8')

def read_wiki_dump(infoboxes, fn):
    print "Reading %s..."%fn
    c = 0
    for line in open(fn):
        items = line.strip('\n').split('\t\t')
        if not len(items) == 2:
            continue
        t, inf = items
        if t in infoboxes:
            props = [DumpProperty(*p.split('::::=')) for p in inf.split(':::::')[-1].split('::::;')]
            infoboxes[t].dump_props = props
    print "%s Finish"%fn
    return infoboxes

def read_wiki_page(infoboxes, fn):
    print "Reading %s..."%fn
    for line in open(fn):
        t, inf = line.strip('\n').split('\t\t')
        if t in infoboxes:
            props = []
            for p in inf.split('::;'):
                if not '::=' in p:
                    continue
                prop, v = p.split('::=')
                if '[[' in prop:
                    ll = pl = ''
                    #items = prop.split('[[')
                    for r in re.findall('\[\[.*\]\]', prop): #property label 的链接可能有多个
                    #for r in items: #property label 的链接可能有多个
                        if '|' in r:
                            pl += r[2:-2].split('|')[-1]
                            ll = r[2:-2].split('|')[0]
                            #ll, pl = prop[2:-2].split('|') #有链接的话第一个是link，第二个是label
                        else:#有链接，两个label一样
                            pl += r[2:-2]
                            ll = r[2:-2]
                else:
                    pl = prop #没有链接，文本就是prop_label
                    ll = ''
                pl = label_filter(pl)
                pl = pl.replace('[','').replace(']','')
                #print pl
                props.append(PageProperty(pl, ll ,v))
            infoboxes[t].page_props = props
    print "%s Finish"%fn
    return infoboxes

def combine_prop(infoboxes):
    """
    默认一个article下的dumpproperty集合一定包含pageproperty
    即pageproperty在dumpproperty有且只有一个对应

    """

    for infobox in infoboxes.values():
        pps = infobox.page_props
        dps = infobox.dump_props
        dps2 = []
        props = []
        for dp in dps:
            dp.value2 = None
            dp.v_vector = None
            if not len(dp.value) or only_chinese(dp.value): #只有中文就不用翻译了
                dp.value2 = dp.value
            else:
                #dp.value2 = translate_en2zh(dp.value)#将英文value翻译成中文后，用相似度
                #print 'Translate %s to %s'%(dp.value, dp.value2)
                dp.value2 = dp.value
            if dp.value2 and len(dp.value2):
                dp.v_vector = text_to_vector(dp.value2)

        for pp in pps:
            matched = False
            for dp in dps:
                if pp.prop_label == dp.dump_label:
                    props.append(Property(pp.prop_label, pp.link_label, dp.dump_label, dp.value)) #保留dump中的value，信息比较正确、完整
                    matched = True
                    break

            if not matched: #用value相似度
                t1 = pp.value
                v1 = text_to_vector(t1)
                mdp = None
                m = 0

                for dp in dps:
                    if not dp.v_vector:
                        continue
                    v2 = dp.v_vector
                    cosine = get_cosine(v1, v2)
                    if cosine > m:
                        m = cosine
                        mdp = dp
                if mdp:
                    matched = True
                    props.append(Property(pp.prop_label, pp.link_label, mdp.dump_label, mdp.value)) #保留dump中的value，信息比较正确、完整
        infobox.props = props
        del infobox.dump_props
        del infobox.page_props
        infoboxes[infobox.title] = infobox

    return infoboxes


def dump_stat(infoboxes):
    props = set()
    for infobox in infoboxes.values():
        for dp in infobox.dump_props:
            props.add(dp.dump_label)
    return len(props)

def page_stat(infoboxes):
    props = set()
    for infobox in infoboxes.values():
        for dp in infobox.page_props:
            props.add(dp.prop_label)
    return len(props)

def fin_stat(infoboxes):
    props = set()
    for infobox in infoboxes.values():
        for dp in infobox.props:
            props.add(dp.prop_label)
    return len(props)

def main():
    zhs = read_titles(ZHWIKI_CRAWL_INFOBOX)
    infoboxes = {}
    for zh in zhs:
        infoboxes[zh] = Infobox(zh)
    infoboxes = read_wiki_dump(infoboxes, ZHWIKI_DUMP_INFOBOX)
    infoboxes = read_wiki_page(infoboxes, ZHWIKI_CRAWL_INFOBOX)

    dnum = dump_stat(infoboxes)
    print "Dump properties:",dnum
    pnum = page_stat(infoboxes)
    print "Page properties:",pnum

    infoboxes = combine_prop(infoboxes)

    cnum = fin_stat(infoboxes)
    print "Combined properties:",pnum

    with open(ZHWIKI_OUTPUT, 'w') as f:
        for infobox in infoboxes.values():
            for p in infobox.props:
                f.write('%s\t%s\t%s\t%s\t%s\n'%(infobox.title, p.prop_label, p.link_label, p.dump_label, p.value))
                f.flush()


if __name__ == "__main__":
    main()
