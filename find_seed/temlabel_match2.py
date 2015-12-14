# -*- coding:utf-8 -*-
import os

"""
Find matched properties in Wikipedia
以template-attribute标识一个attribute
首先，根据attribute的共现程度，找出相似的template，合并成一个(记录数据)
1. 同一个template下template label相同的
2. cross-template下template label相同的
3. cross-instance下template label相同的
4. cross-instance下value相同的
"""

DIR = "/home/keg/data/infobox"
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-enwiki-template-triple.dat.uniq")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-zhwiki-template-triple.dat.uniq")
MATCHED_TEMPLATE_LABEL1 = os.path.join(DIR, "matched-template-label-2-1.dat")
MATCHED_TEMPLATE_LABEL2 = os.path.join(DIR, "matched-template-label-2-2.dat")
MATCHED_TEMPLATE_LABEL3 = os.path.join(DIR, "matched-template-label-2-3.dat")
MATCHED_TEMPLATE_LABEL4 = os.path.join(DIR, "matched-template-label-2-4.dat")
MATCHED_TEMPLATE_LABEL_ALL = os.path.join(DIR, "matched-template-label-all-2.dat")
MATCHED_TEMPLATE = os.path.join(DIR, "template.cl")
MATCHED_INSTANCE = ""
ENWIKI_INFOBOX = ""
ZHWIKI_INFOBOX = ""

class TempalteAttribute:
    def __init__():
        pass

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
                    all_matched[tem+'###'+prop_label] = tem+'###'+zhwiki[tem][tem_label]
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
                    all_matched[tem_en+'###'+prop_label] = tem_zh+'###'+zhwiki[tem_zh][tem_label]
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
            tem_en = enwiki_tem_label[tem_en]
            tem_zh = zhwiki_tem_label[tem_zh]
            if tem_en in matched_tem and tem_zh == matched_tem[tem_en]:
                continue
            print "Matched Templates in Matched Instances", tem_en, tem_zh
            for tem_label, prop_label in enwiki[tem_en].iteritems():
                if tem_label in zhwiki[tem_zh]:
                    fw.write('%s\t%s\t%s\t%s\n'%(tem_en+'###'+tem_zh, tem_label, tem_en+'###'+prop_label, tem_zh+'###'+zhwiki[tem_zh][tem_label]))
                    all_matched[tem_en+'###'+prop_label] = tem_zh+'###'+zhwiki[tem_zh][tem_label]
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
        fw.write(en+'\t'+zh+'\n')
    fw.close()

def merge_similar_tem(tem):
    """
    Find the similar tempaltes and merge them into one
    """
    
    tem_label = {}
    label_tems = {}
    tems = set(tem.keys())
    for t1, d1 in tem.iteritems():
        for t2, d2 in tem.iteritems():
            if not t2 in tems: #已经有分组
                continue
            s = len(set(d1.keys()) & set(d2.keys()))*1.0/len(set(d1.keys())|set(d2.keys())) 
            if s > 0.7:
                #print t1, t2, s, len(set(d1.keys()) & set(d2.keys())), len(set(d1.keys())|set(d2.keys()))
                #print t1, t2, s
                label = None
                if not t2 in tem_label and not t1 in tem_label:
                    label = t2 if 'sandbox' in t1 else t1
                    label_tems[label] = set()
                elif t1 in tem_label:
                    label = tem_label[t1]
                else:
                    label = tem_label[t2]
                if t1 in tems:
                    tems.remove(t1)
                if t2 in tems:
                    tems.remove(t2)
                label_tems[label].add(t1)
                label_tems[label].add(t2)
                tem_label[t1] = label 
                tem_label[t2] = label 
    print "tems:",len(tems)
    for l, tems in label_tems.iteritems():
        if 'sandbox' in l:
            if len(tems) == 1:
                continue
            for t in tems:
                if not 'sandbox' in t:
                    label_tems[t] = label_tems[l]
                    label_tems.pop(l)
                    break
    print "Final Templates Set:", len(label_tems)
    return tem_label, label_tems

    
matched_tem = dict((line.strip('\n').split('\t')) for line in open(MATCHED_TEMPLATE))
print "ALL matched templates:",len(matched_tem)
matched_ins = dict((line.strip('\n').split('\t')) for line in open(MATCHED_INSTANCE))

enwiki = read_properties(ENWIKI_TEMPLATE_LABEL)
#case_enwiki = dict((k.lower(), k) for k in enwiki) #忽略大小写
zhwiki = read_properties(ZHWIKI_TEMPLATE_LABEL)
#case_zhwiki = dict((k.lower(), k) for k in zhwiki) #忽略大小写

enwiki_tem_label, enwiki_label_tems = merge_similar_tem(enwiki)
for l, tems in sorted(enwiki_label_tems.items()):
    print l, tems
    #print l
print "Final Templates Set:", len(enwiki_label_tems)
zhwiki_tem_label, zhwiki_label_tems = merge_similar_tem(zhwiki)
for l, tems in sorted(zhwiki_label_tems.items()):
    print l, tems
    #print l
print "Final Templates Set:", len(zhwiki_label_tems)

print "Origin enwiki templates:",len(enwiki)
for tem in enwiki.keys():
    temlabel = enwiki_tem_label[tem]
    if temlabel == tem:
        continue
    enwiki[temlabel].update(enwiki[tem])
    enwiki.pop(tem)
print "Left enwiki templates:",len(enwiki)

print "Origin zhwiki templates:",len(zhwiki)
for tem in zhwiki.keys():
    temlabel = zhwiki_tem_label[tem]
    if temlabel == tem:
        continue
    zhwiki[temlabel].update(zhwiki[tem])
    zhwiki.pop(tem)
print "Left zhwiki templates:",len(zhwiki)

print "ALL enwiki template attributes:", sum([len(v) for v in enwiki.values()])
print "ALL zhwiki template attributes:", sum([len(v) for v in zhwiki.values()])

origin_matched_tem, matched_tem = matched_tem, {}
for t1, t2 in origin_matched_tem.items():
    if t1 in enwiki_tem_label and t2 in zhwiki_tem_label:
        matched_tem[enwiki_tem_label[t1]] = zhwiki_tem_label[t2]


all_matched = {}

enwiki_infobox, enwiki_infobox_tem = read_infoboxes(ENWIKI_INFOBOX, matched_ins)
zhwiki_infobox, zhwiki_infobox_tem = read_infoboxes(ZHWIKI_INFOBOX, matched_ins)

find_matched_1()
print "Matched templates with different label:",len(matched_tem)
print "ALL Matched properties:",len(all_matched)
find_matched_2()
print "ALL Matched properties:",len(all_matched)
find_matched_3()
#find_matched_4()
#merge()
