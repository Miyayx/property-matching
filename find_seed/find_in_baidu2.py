# -*- coding:utf-8 -*-
import sys,os

sys.path.append('..')
from utils.logger import *
import utils.label as label
initialize_logger('./find_enwiki_baidu.log')

"""
通过已有的wikipedia matched properties 从百度中找到对应的property
Property以Template:Attribute的形式标识，从百度中找到对应property也应带有领域信息
输入：
    1. 初步的百度template(baidu_template.py获得), 即enwiki template与其对应的baidu attribute(该template下attribute候选集)
    2. 已匹配的enwiki，zhwiki attribute
    3. enwiki，zhwiki template集合
输出：
    领域下(template)下，匹配的enwiki与baidu attribute对
"""

DIR = "/home/keg/data/infobox"
MATCHED_TEMPLATE_LABEL_ALL = os.path.join(DIR, "matched-template-label-all-2.dat")
ENWIKI_MERGED_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-merged-template-label.dat")
ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE = os.path.join(DIR, "enwiki-template-baidu-attribute.dat")
ENWIKI_BAIDU_MATCHED_PROPERTY = os.path.join(DIR, "enwiki-baidu-matched-property-2.dat")


def read_merged_template(fn):
    print "read_merged_template"
    return dict((line.strip('\n').split('\t')) for line in open(fn))

def read_wiki_matched_attributes(fn):
    print "read_wiki_matched_attributes"
    tem_zh_en = {}
    for line in open(MATCHED_TEMPLATE_LABEL_ALL):
        en, zh = line.strip('\n').split('\t')
        tem, en = en.split('###')
        zh = zh.split('###')[-1]
        en = label.clean_label(en)
        zh = label.clean_label(zh)
        if not tem in tem_zh_en:
            tem_zh_en[tem] = {}
        tem_zh_en[tem][zh] = en
    return tem_zh_en

def find_in_baidu():
    """
    1. 读取enwiki template集合
    2. 读取已匹配enwiki，zhwiki attribute
    3. 在读取baidu template属性的过程中，通过enwiki template label找到对应的merged template label，进而找到对应的enwiki template与其属性, 通过中文字段匹配
    """
    
    enwiki_tem_label = read_merged_template(ENWIKI_MERGED_TEMPLATE_LABEL)
    case_tem_label = {}
    for tem, label in enwiki_tem_label.iteritems():
        case_tem_label[tem.lower()] = label
    tem_zh_en = read_wiki_matched_attributes(MATCHED_TEMPLATE_LABEL_ALL)

    fw = open(ENWIKI_BAIDU_MATCHED_PROPERTY, 'w')
    for line in open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE):
        tem, attrs = line.strip('\n').split('\t')
        if not tem.lower() in case_tem_label:
            continue
        print tem
        tlabel = case_tem_label[tem]
        for a in attrs.split(':::'):
            if tlabel in tem_zh_en and a in tem_zh_en[tlabel]:
                fw.write("%s\t%s\t%s\n"%(tem, tem_zh_en[tlabel][a], a))
    fw.close()

if __name__ == "__main__":
    find_in_baidu()

        
