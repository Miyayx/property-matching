# -*- coding:utf-8 -*-
import os
import codecs

import sys
sys.path.append('..')
from utils.logger import *
from render_label_parser.fileio import *
initialize_logger('./temlabel_match2.log')

"""
需要跨语言链接：
    template.cl文件从template_cl.py获得


中英文维基内部的属性对齐
与match_temlabel.py不一样的是：以template-attribute标识一个attribute

首先，根据attribute集合的相似度，找出相似的template，合并成一个(记录数据)
1. 同一个template下template label相同的
2. cross-template下template label相同的
3. cross-instance下template label相同的
4. cross-instance下value相同的
"""

#DIR = "/home/keg/data/infobox"
#DIR = "/home/xlore/server36/infobox"
DIR = "/data/xlore20160223/Template"

#ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-enwiki-template-triple.dat.uniq")
#ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-zhwiki-template-triple.dat.uniq")
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-20160305-template-triple.dat")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-20160203-template-triple.dat")

ENWIKI_INHERIT_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-20160305-inherit-template-triple.dat")
ZHWIKI_INHERIT_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-20160203-inherit-template-triple.dat")

MATCHED_TEMPLATE_LABEL1 = os.path.join(DIR, "matched-template-label-2-1.dat")
MATCHED_TEMPLATE_LABEL2 = os.path.join(DIR, "matched-template-label-2-2.dat")
MATCHED_TEMPLATE_LABEL3 = os.path.join(DIR, "matched-template-label-2-3.dat")
MATCHED_TEMPLATE_LABEL4 = os.path.join(DIR, "matched-template-label-2-4.dat")
MATCHED_TEMPLATE_LABEL_ALL = os.path.join(DIR, "matched-template-label-all-2.dat")

MATCHED_TEMPLATE = os.path.join(DIR, "template.cl")
MATCHED_INSTANCE = os.path.join(DIR, "enwiki.zh.en.title.cl")

#ENWIKI_INFOBOX = "/home/xlore/disk2/raw.wiki/enwiki-infobox-new.dat"
#ZHWIKI_INFOBOX = "/home/xlore/disk2/raw.wiki/zhwiki-infobox-new.dat"

ENWIKI_INFOBOX = "/data/xlore20160223/wikiExtractResult/enwiki-infobox-tmp-template-replaced.dat"
ZHWIKI_INFOBOX = "/data/xlore20160223/wikiExtractResult/zhwiki-infobox-tmp-template-replaced.dat"

ENWIKI_MERGED_TEMPLATE = os.path.join(DIR, "enwiki-merged-template-label.dat")
ZHWIKI_MERGED_TEMPLATE = os.path.join(DIR, "zhwiki-merged-template-label.dat")

def find_matched_1():
    """
    1. 同一个template下template label相同的
    """
    fw = codecs.open(MATCHED_TEMPLATE_LABEL1, 'w', 'utf-8')
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

    fw = codecs.open(MATCHED_TEMPLATE_LABEL2, 'w', 'utf-8')
    for tem_en, tem_zh in matched_tem.iteritems(): 
        if tem_en in enwiki and tem_zh in zhwiki:
            #print "Matched Templates:", tem_en, tem_zh
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
    fw = codecs.open(MATCHED_TEMPLATE_LABEL3, 'w', 'utf-8')
    for ins_en, ins_zh in matched_ins.iteritems():
        if ins_en in enwiki_infobox_tem and ins_zh in zhwiki_infobox_tem:
            tem_en = enwiki_infobox_tem[ins_en]
            tem_zh = zhwiki_infobox_tem[ins_zh]
            if tem_en == tem_zh:
                continue

            # 这里认为template名称意见经过处理，不需要判断大小写，redirect一类的
            #if not tem_en in case_enwiki_tem_label or not tem_zh in case_zhwiki_tem_label:
            #    continue
            #tem_en = case_enwiki_tem_label[tem_en]
            #tem_zh = case_zhwiki_tem_label[tem_zh]

            if tem_en in matched_tem and tem_zh == matched_tem[tem_en]:
                continue
            print "Matched Templates in Matched Instances", tem_en, tem_zh
            if not tem_en in enwiki or not tem_zh in zhwiki:
                print tem_en, 'not in enwiki'
                print tem_zh, 'not in zhwiki'
                continue
            for tem_label, prop_label in enwiki[tem_en].iteritems():
                if tem_label in zhwiki[tem_zh]:
                    fw.write('%s\t%s\t%s\t%s\n'%(tem_en+'###'+tem_zh, tem_label, tem_en+'###'+prop_label, tem_zh+'###'+zhwiki[tem_zh][tem_label]))
                    all_matched[tem_en+'###'+prop_label] = tem_zh+'###'+zhwiki[tem_zh][tem_label]
                    fw.flush()
    fw.close()

def find_matched_4():
    """
    4. cross-instance下value指向同一个article的
    """
    fw = codecs.open(MATCHED_TEMPLATE_LABEL4, 'w', 'utf-8')
    for ins_en, ins_zh in matched_ins.iteritems():
        if ins_en in enwiki_infobox_tem and ins_zh in zhwiki_infobox_tem:
            tem_en = enwiki_infobox_tem[ins_en]
            tem_zh = zhwiki_infobox_tem[ins_zh]

            if tem_en == tem_zh:
                continue
            if tem_en in matched_tem and tem_zh == matched_tem[tem_en]:
                continue

            print "Matching Value in Matched Instances", tem_en, tem_zh
            info_en = enwiki_infobox[ins_en]
            info_zh = zhwiki_infobox[ins_zh]
            for k, v in info_en.iteritems():
                if "[[" in v:
                    v = v[v.index('[[')+2: v.index(']]')]
                    v = v.split('|')[0] 
                if len(v) > 0 and v in matched_ins: #如果确定这个property有指向跨语言链接实体的value，再去看看中文里有没有跟它value相同的
                    for k2, v2 in info_zh.iteritems():
                        if "[[" in v2:
                            v2 = v2[v2.index('[[')+2: v2.index(']]')]
                            v2 = v2.split('|')[0] 
                        if v == v2 or matched_ins[v] == v2:
                            #print "%s,%s,%s,%s"%(v, v2, k, k2)
                            fw.write('%s\t%s\t%s\t%s\n'%(tem_en+'###'+tem_zh, '###', tem_en+'###'+k, tem_zh+'###'+k2))
                            all_matched[tem_en+'###'+k] = tem_zh+'###'+k
                            fw.flush()

    fw.close()

def merge():
    """
    cat file1 file2 file3 file4 > file-all
    """
    fw = codecs.open(MATCHED_TEMPLATE_LABEL_ALL, 'w', 'utf-8')
    for en, zh in sorted(all_matched.iteritems()):
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
    #print "tems:",len(tems)
    for l, tems in label_tems.iteritems():
        if 'sandbox' in l:
            if len(tems) == 1:
                continue
            for t in tems:
                if not 'sandbox' in t:
                    label_tems[t] = label_tems[l]
                    label_tems.pop(l)
                    break
    #print "Final Templates Set:", len(label_tems)
    return tem_label, label_tems

import time

start = time.time()
    
matched_tem = dict((line.strip('\n').split('\t')) for line in codecs.open(MATCHED_TEMPLATE, 'r', 'utf-8'))
print "ALL matched templates:",len(matched_tem)
matched_ins = dict((line.strip('\n').split('\t')) for line in codecs.open(MATCHED_INSTANCE, 'r', 'utf-8'))

enwiki = read_template_triple(ENWIKI_TEMPLATE_LABEL)
enwiki.update(read_template_triple(ENWIKI_INHERIT_TEMPLATE_LABEL))
zhwiki = read_template_triple(ZHWIKI_TEMPLATE_LABEL)
zhwiki.update(read_template_triple(ZHWIKI_INHERIT_TEMPLATE_LABEL))

#enwiki_tem_label, enwiki_label_tems = merge_similar_tem(enwiki)
##for l, tems in sorted(enwiki_label_tems.items()):
##    print l, tems
#print "Final Templates Set:", len(enwiki_label_tems)
#with codecs.open(ENWIKI_MERGED_TEMPLATE, 'w', 'utf-8') as fw:
#    for tem, l in enwiki_tem_label.iteritems():
#        fw.write("%s\t%s\n"%(tem, l))
#
#zhwiki_tem_label, zhwiki_label_tems = merge_similar_tem(zhwiki)
##for l, tems in sorted(zhwiki_label_tems.items()):
##    print l, tems
#print "Final Templates Set:", len(zhwiki_label_tems)
#with codecs.open(ZHWIKI_MERGED_TEMPLATE, 'w', 'utf-8') as fw:
#    for tem, l in zhwiki_tem_label.iteritems():
#        fw.write("%s\t%s\n"%(tem, l))
#
#print "Origin enwiki templates:",len(enwiki)
#for tem in enwiki.keys():
#    temlabel = enwiki_tem_label[tem]
#    if temlabel == tem:
#        continue
#    enwiki[temlabel].update(enwiki[tem])
#    enwiki.pop(tem)
#print "Left enwiki templates:",len(enwiki)
#
#print "Origin zhwiki templates:",len(zhwiki)
#for tem in zhwiki.keys():
#    temlabel = zhwiki_tem_label[tem]
#    if temlabel == tem:
#        continue
#    zhwiki[temlabel].update(zhwiki[tem])
#    zhwiki.pop(tem)
#print "Left zhwiki templates:",len(zhwiki)

#case_enwiki_tem_label = dict((k.lower(), v) for k, v in enwiki_tem_label.items()) #忽略大小写
#case_zhwiki_tem_label = dict((k.lower(), v) for k, v in zhwiki_tem_label.items()) #忽略大小写

print "ALL enwiki template attributes:", sum([len(v) for v in enwiki.values()])
print "ALL zhwiki template attributes:", sum([len(v) for v in zhwiki.values()])

#origin_matched_tem, matched_tem = matched_tem, {}
#for t1, t2 in origin_matched_tem.items():
#    if t1 in enwiki_tem_label and t2 in zhwiki_tem_label:
#        matched_tem[enwiki_tem_label[t1]] = zhwiki_tem_label[t2]

all_matched = {}

find_matched_1()
print "Matched templates with different label:",len(matched_tem)
print "After method1, ALL Matched properties:",len(all_matched)
find_matched_2()
print "After method2, ALL Matched properties:",len(all_matched)

enwiki_infobox_tem, enwiki_infobox = read_wiki_infobox(ENWIKI_INFOBOX)
zhwiki_infobox_tem, zhwiki_infobox = read_wiki_infobox(ZHWIKI_INFOBOX)
matched_ins_enwiki = set(matched_ins.values())
matched_ins_zhwiki = set(matched_ins.keys())
enwiki_infobox_tem = {k: v for k, v in enwiki_infobox_tem.iteritems() if k in matched_ins_enwiki}
enwiki_infobox = {k: v for k, v in enwiki_infobox.iteritems() if k in matched_ins_enwiki}
zhwiki_infobox_tem = {k: v for k, v in zhwiki_infobox_tem.iteritems() if k in matched_ins_zhwiki}
zhwiki_infobox = {k: v for k, v in zhwiki_infobox.iteritems() if k in matched_ins_zhwiki}

find_matched_3()
print "After method3, ALL Matched properties:",len(all_matched)
find_matched_4()
print "After method4, ALL Matched properties:",len(all_matched)

merge()

print 'Time Consuming:',time.time()-start
