#!/usr/bin/python
# -*- utf-8 -*-

from models import *
from utils import *

ENWIKI_DUMP_INFOBOX = '/home/keg/data/wikiraw/enwiki-infobox-tmp.dat'
ZHWIKI_DUMP_INFOBOX = '/home/keg/data/wikiraw/zhwiki-infobox-tmp.dat'
ENWIKI_CRAWL_INFOBOX = '/home/keg/data/infobox/enwiki-infobox-scrapy.dat'
ZHWIKI_CRAWL_INFOBOX = '/home/keg/data/infobox/zhwiki-infobox-scrapy.dat'

def read_titles(fn):
    return [line.split('\t\t')[0] for line in open(fn)]
    
def read_wiki_dump(infoboxes, fn):
    for line in open(fn):
        t, inf = line.strip('\n').split('\t\t')
        if t in infoboxes:
            props = [DumpProperty(p.split('::::=')) for p in inf.split('::::')]
            infoboxes[t].dump_props = props

def read_wiki_page(infoboxes, fn):
    for line in open(fn):
        t, inf = line.strip('\n').split('\t\t')
        if t in infoboxes:
            props = []
            for p in inf.split(':::'):
                prop, v = p.split('::=')
                if '[[' in prop:
                    if '|' in prop:
                        ll, pl = prop[2:-2].split('|') #有链接的话第一个是link，第二个是label
                    else:
                        ll, pl = prop[2:-2] #有链接，两个label一样
                else:
                    pl = prop #没有链接，文本就是prop_label
                    ll = ''
            props.append(PageProperty(pl, ll ,v))
            infoboxes[t].page_props = props

def combine_prop(infoboxes):
    """
    默认一个article下的dumpproperty集合一定包含pageproperty
    即pageproperty在dumpproperty有且只有一个对应
    
    """
    for infobox in infoboxes.values():
        pps = infobox.page_props
        dps = infobox.dump_props
        props = []
        for pp in pps:
            matched = False
            for dp in dps:
                if pp.prop_label == dp.dump_label:
                    props.append(Property(pp.prop_label, pp.link_label, dp.dump_label, dp.value)) #保留dump中的value，信息比较正确、完整
                    matched = True
                    break

            if not matched:
                t1 = pp.value
                v1 = text_to_vector(t1)
                mdp = None
                m = 0
                
                for dp in dps:
                    t2 = dp.value
                    v2 = text_to_vector(t2)
                    cosine = get_cosine(vector1, vector2)
                    if cosine > m:
                        m = cosine
                        mdp = dp
                props.append(Property(pp.prop_label, pp.link_label, mdp.dump_label, mdp.value)) #保留dump中的value，信息比较正确、完整
        infobox.props = props
        del infobox.dump_props
        del infobox.page_props
        infoboxes[infobox.title] = infobox

    return infoboxes


def dump_stat(infoboxes):
    props = set()
    for infobox in infoboxes:
        for dp in infobox.dump_props:
            props.add(dp.dump_label)
    return len(props)

def page_stat(infoboxes):
    props = set()
    for infobox in infoboxes:
        for dp in infobox.page_props:
            props.add(dp.prop_label)
    return len(props)

def main():
    zhs = read_titles(ZHWIKI_CRAWL_INFOBOX)
    infoboxes = {}
    for zh in zhs:
        infoboxes[zh] = Infobox(zh)
    read_wiki_dump(infoboxes, ZHWIKI_DUMP_INFOBOX)
    read_wiki_page(infoboxes, ZHWIKI_CRAWL_INFOBOX)

    dnum = dump_stat(infoboxes)
    pnum = page_stat(infoboxes)

    combine_prop(infoboxes)

if __name__ == "__main__":
    main()
    
        
