# -*- coding:utf-8 -*-
import os

"""
Find matched properties in Wikipedia
1. 同一个template下template label相同的
2. cross-template下template label相同的
3. cross-instance下template label相同的
4. cross-instance下value相同的
"""

DIR = "/home/keg/data/infobox"
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-template-triple.dat.uniq")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-template-triple.dat.uniq")
MATCHED_TEMPLATE_LABEL1 = os.path.join(DIR, "matched-template-label-1.dat")
MATCHED_TEMPLATE_LABEL2 = os.path.join(DIR, "matched-template-label-2.dat")
MATCHED_TEMPLATE_LABEL3 = os.path.join(DIR, "matched-template-label-3.dat")
MATCHED_TEMPLATE_LABEL4 = os.path.join(DIR, "matched-template-label-4.dat")
MATCHED_TEMPLATE_LABEL_ALL = os.path.join(DIR, "matched-template-label-all.dat")
MATCHED_TEMPLATE = os.path.join(DIR, "template.cl")
MATCHED_INSTANCE = ""
ENWIKI_INFOBOX = ""
ZHWIKI_INFOBOX = ""

def read_properties(fn):
    d = {}
    for line in open(fn):
        tem, tem_label, _, prop_label = line.strip('\n').split('\t')
        if not tem in d:
            d[tem] = {}
        if tem_label in d[tem]:
            continue
        d[tem][tem_label] = prop_label
    return d

def read_infoboxes(fn, matched_ins):
    d = {}
    d2 = {}
    for line in open(fn):
        title, info = line.strip('\n').split('\t\t')
        if not title in matched_ins: #没有crosslingual的instance就不要了
            continue
        tem, infobox = info.split(':::::')
        tem = 'template:'+tem
        
        d[title] = {}
        d2[title] = tem
        for kv in infobox.split('::::;'):
            k, v = kv.split(':::::')
            d[(title, tem)][k] = v
    return d, d2

def find_matched_1():
    """
    1. 同一个template下template label相同的
    """
    fw = open(MATCHED_TEMPLATE_LABEL1, 'w')
    for tem, d in enwiki.iteritems():
        if tem in zhwiki:
            for tem_label, prop_label in enwiki[tem].iteritems():
                if tem_label in zhwiki[tem]:
                    fw.write('%s\t%s\t%s\t%s\n'%(tem, tem_label, prop_label, zhwiki[tem][tem_label]))
                    all_matched[prop_label] = zhwiki[tem][tem_label]
                    fw.flush()
            if tem in matched_tem: #中英两个template名字相同，之后不作处理
                matched_tem.pop(tem)
    fw.close()

def find_matched_2():
    """
    2. cross-template下template label相同的
    """

    fw = open(MATCHED_TEMPLATE_LABEL2, 'w')
    for tem_en, tem_zh in matched_tem.iteritems(): 
        if tem_en in enwiki and tem_zh in zhwiki:
            print "Matched Templates:", tem_en, tem_zh
            if tem_en == tem_zh:
                print "Sample Template, Pass"
                continue
            for tem_label, prop_label in enwiki[tem_en].iteritems():
                if tem_label in zhwiki[tem_zh]:
                    fw.write('%s\t%s\t%s\t%s\n'%(tem_en+'###'+tem_zh, tem_label, prop_label, zhwiki[tem_zh][tem_label]))
                    all_matched[prop_label] = zhwiki[tem_zh][tem_label]
                    fw.flush()
    fw.close()

def find_matched_3():
    """
    3. cross-instance下template label相同的
    """
    fw = open(MATCHED_TEMPLATE_LABEL3, 'w')
    for ins_en, ins_zh in matched_ins.iteritems():
        if ins_en in enwiki_infobox_tem and ins_zh in zhwiki_infobox_tem:
            tem_en = enwiki_infobox_tem[ins_en]
            tem_zh = zhwiki_infobox_tem[ins_zh]
            if tem_en == tem_zh:
                continue
            tem_en = case_enwiki[tem_en]
            tem_zh = case_zhwiki[tem_zh]
            if tem_en in matched_tem and tem_zh == matched_tem[tem_en]:
                continue
            print "Matched Templates in Matched Instances", tem_en, tem_zh
            for tem_label, prop_label in enwiki[tem_en].iteritems():
                if tem_label in zhwiki[tem_zh]:
                    fw.write('%s\t%s\t%s\t%s\n'%(tem, tem_label, prop_label, zhwiki[tem_zh][tem_label]))
                    fw.flush()
    fw.close()

def find_matched_4():
    """
    4. cross-instance下value相同的
    """
    fw = open(MATCHED_TEMPLATE_LABEL4, 'w')
    for ins_en, ins_zh in matched_ins.iteritems():
        if ins_en in enwiki_infobox and ins_zh in zhwiki_infobox:
            tem_en = enwiki_infobox_tem[ins_en]
            tem_zh = zhwiki_infobox_tem[ins_zh]

    fw.close()

def merge():
    """
    cat file1 file2 file3 file4 > file-all
    """
    fw = open(MATCHED_TEMPLATE_LABEL_ALL, 'w')
    for en, zh in all_matched.iteritems():
        fw.write(en+'\t'+zh)
    fw.close()
        
    
matched_tem = dict((line.strip('\n').split('\t')) for line in open(MATCHED_TEMPLATE))
print "ALL matched templates:",len(matched_tem)
#matched_ins = dict((line.strip('\n').split('\t')) for line in open(MATCHED_INSTANCE))

enwiki = read_properties(ENWIKI_TEMPLATE_LABEL)
case_enwiki = dict((k.lower(), k) for k in enwiki)
zhwiki = read_properties(ZHWIKI_TEMPLATE_LABEL)
case_zhwiki = dict((k.lower(), k) for k in zhwiki)

all_matched = {}

#enwiki_infobox, enwiki_infobox_tem = read_infoboxes(ENWIKI_INFOBOX, matched_ins)
#zhwiki_infobox, zhwiki_infobox_tem = read_infoboxes(ZHWIKI_INFOBOX, matched_ins)

find_matched_1()
print "Matched templates with different label:",len(matched_tem)
print "ALL Matched properties:",len(all_matched)
find_matched_2()
print "ALL Matched properties:",len(all_matched)
#find_matched_3()
#find_matched_4()
merge()
