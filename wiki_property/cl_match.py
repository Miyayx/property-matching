#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
Find existed crosslingual matched properties in wiki
"""

import os

DIR = '/home/www/lmy_36mnt/data'

EN_ZH_CL = os.path.join(DIR, 'wikiraw/en_zh.txt')
ENWIKI_INFOBOX_MATCHED = os.path.join(DIR, 'infobox/enwiki-infobox-matched.dat')
ZHWIKI_INFOBOX_MATCHED = os.path.join(DIR, 'infobox/zhwiki-infobox-matched.dat')
OUTPUT = os.path.join(DIR, 'infobox/wiki-matched-props.dat')

SIM = 0.8


def read_en_zh_cl(fn):
    return [line.strip('\n').split('\t') for line in open(fn)]

def load_infoboxes(fn):
    infoboxes = {}
    for line in open(fn):
        title, pl, ll, dl, v = line.strip('\n').split('\t')
        box = infoboxes.get(title, Infobox(title))
        box.props.append(Property(pl, ll, dl, v))
        infoboxes[title] = box
        
    return infoboxes

def add_vector(box):
    for ep in box.props:
        value2 = None
        ep.v_vector = None
        if not len(ep.value) or only_chinese(ep.value): #只有中文就不用翻译了
            value2 = dp.value
        else:
            #value2 = translate_en2zh(ep.value)#将英文value翻译成中文后，用相似度
            #print 'Translate %s to %s'%(ep.value, value)
            value2 = dp.value
        if value2 and len(value2):
            ep.v_vector = text_to_vector(value2)
    return box

def cl_match(enbox, zhbox ):
    mbox = MatchedInfobox(en=enbox.title, zh=zhbox.title)
    
    enbox = add_vector(enbox)
    zhbox = add_vector(zhbox)

    for ep in enbox.props:
        for zp in zhbox.props:
            if ep.dump_label == zp.dump_label:
                mbox.m_props.append((ep.prop_label, zp.prop_label))
                zhbox.props.pop(zp)
                enbox.props.pop(ep)
                break
            elif is_matched(ep.link_label, zp.link_label):
                mbox.m_props.append((ep.prop_label, zp.prop_label))
                zhbox.props.pop(zp)
                enbox.props.pop(ep)
                break
            elif ep.v_vector and zp.v_vector:
                cosine = get_cosine(ep.v_vector, zp.v_vector)
                if cosine > SIM:
                    mbox.m_props.append((ep.prop_label, zp.prop_label))
                    zhbox.props.pop(zp)
                    enbox.props.pop(ep)
                    break
    return mbox

def prop_stat(boxes):
    en_set = set()
    zh_set = set()
    cl_set = set()
    for box in boxes:
        for en, zh in box.props:
            en_set.add(en)
            zh_set.add(zh)
            cl_set.add(en+'\t'+zh)
    return len(en_set), len(zh_set), len(cl_set), cl_set

def main():
    enboxes = load_infoboxes(ENWIKI_INFOBOX_MATCHED)
    zhboxes = load_infoboxes(ZHWIKI_INFOBOX_MATCHED)
    en_zh = read_en_zh_cl(EN_ZH_CL)
    en_zh = [ i for i in en_zh if i[0] in enboxes]
    en_zh = [ i for i in en_zh if i[1] in zhboxes]

    boxes = []
    for en, zh in en_zh:
        box = cl_match(enboxes[en], zhboxes[zh])
        boxes.append(box)

    en_num, zh_num, cl_num, cl_set = prop_stat(boxes)
    print "ennum:%d, zhnum:%d, clnum:%d"%(en_num, zh_num, cl_num)

    with open(OUTPUT) as f:
        for cl in sorted(cl_set):
            f.write(cl+'\n')


