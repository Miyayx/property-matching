#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
Find existed crosslingual matched properties in wiki
"""

import os

from models import *
from utils import *

DIR = '/home/www/lmy_36mnt/data'

EN_ZH_CL = os.path.join(DIR, 'wikiraw/en_zh.txt')
ENWIKI_INFOBOX_MATCHED = os.path.join(DIR, 'infobox/enwiki-infobox-matched.dat')
ZHWIKI_INFOBOX_MATCHED = os.path.join(DIR, 'infobox/zhwiki-infobox-matched.dat')
OUTPUT = os.path.join(DIR, 'infobox/wiki-matched-props.dat')

SIM = 0.8

def read_zh_en_cl(fn):
    return [line.strip('\n').split('\t') for line in open(fn) if len(line.split('\t')) > 1]

def load_infoboxes(fn):
    infoboxes = {}
    for line in open(fn):
        title, pl, ll, dl, v = line.strip('\n').split('\t')
        box = infoboxes.get(title, Infobox(title))
        box.props.append(Property(pl, ll, dl, v))
        infoboxes[title] = box

    return infoboxes

def add_vector(box):
    """
    Add text vector of value to an infobox for futher similarity calculation in loop
    """
    for ep in box.props:
        value2 = None
        ep.v_vector = None
        if not len(ep.value) or only_chinese(ep.value): #只有中文就不用翻译了
            value2 = ep.value
        else:
            #value2 = translate_en2zh(ep.value)#将英文value翻译成中文后，用相似度
            #print 'Translate %s to %s'%(ep.value, value)
            value2 = ep.value
        if value2 and len(value2):
            ep.v_vector = text_to_vector(value2, lan='zh')
    return box


def cl_match(enbox, zhbox):
    print "Tring to match %s and %s"%(enbox.title, zhbox.title)
    mbox = MatchedInfobox(en=enbox.title, zh=zhbox.title)

    enbox = add_vector(enbox)
    zhbox = add_vector(zhbox)

    for ep in enbox.props:
        if ep.matched: continue #已经有匹配了就不做处理了
        for zp in zhbox.props:
            if zp.matched: continue
            if ep.dump_label == zp.dump_label: #template label相同
                mbox.m_props.append((ep.prop_label, zp.prop_label))
                ep.matched = True
                zp.matched = True
                break
            elif is_matched(ep.link_label, zp.link_label): #链接同一个跨语言实例
                mbox.m_props.append((ep.prop_label, zp.prop_label))
                ep.matched = True
                zp.matched = True
                break
            elif ep.v_vector and zp.v_vector: #value相似度比较高
                cosine = get_cosine(ep.v_vector, zp.v_vector)
                if cosine > SIM:
                    mbox.m_props.append((ep.prop_label, zp.prop_label))
                    ep.matched = True
                    zp.matched = True
                    break
    return mbox

def prop_stat(boxes):
    """
    统计
    """
    en_set = set()
    zh_set = set()
    cl_set = set()
    for box in boxes:
        for en, zh in box.m_props:
            en_set.add(en)
            zh_set.add(zh)
            cl_set.add(en+'\t'+zh)
    return len(en_set), len(zh_set), len(cl_set), cl_set

def is_matched(en, zh):
    return True if en in en_zh_map and zh == en_zh_map[en] else False

def main():
    import time
    s_time = time.time()

    enboxes = load_infoboxes(ENWIKI_INFOBOX_MATCHED)
    print len(enboxes),"enboxes"
    zhboxes = load_infoboxes(ZHWIKI_INFOBOX_MATCHED)
    print len(zhboxes),"zhboxes"
    zh_en = read_zh_en_cl(EN_ZH_CL)
    global en_zh_map
    en_zh_map = dict((en,zh) for zh,en in zh_en)# zh和en label的hashmap，方便后面查找一个中英文对是否match

    # 只保留有infobox的跨语言链接对
    zh_en = [ i for i in zh_en if i[0] in zhboxes]
    zh_en = [ i for i in zh_en if i[1] in enboxes]
    print "",len(zh_en)

    boxes = []
    for i in xrange(len(zh_en[:])):
        print i
        zh, en = zh_en[i] #对每一对跨语言链接instance，对齐其中的infobox属性
        box = cl_match(enboxes[en], zhboxes[zh])
        boxes.append(box)

    en_num, zh_num, cl_num, cl_set = prop_stat(boxes)
    print "ennum:%d, zhnum:%d, clnum:%d"%(en_num, zh_num, cl_num)

    with open(OUTPUT, 'w') as f:
        for cl in sorted(cl_set):
            f.write(cl+'\n')

    print "Time Consuming:",time.time()-s_time

if __name__=="__main__":
    main()
