#-*- coding:utf-8 -*-

import codecs
import sys,os
import re

from difflib import SequenceMatcher
import Levenshtein

sys.path.append('..')
from utils.logger import *
import utils.label as label
initialize_logger('./find_zhwiki_baidu.log')

ZHWIKI_INFOBOX = "/data/xlore20160223/wikiExtractResult/zhwiki-infobox-tmp-infobox-replaced.dat"
BAIDU_INFOBOX  = "/data/baidu/baidu-title-property.dat"
ZHWIKI_BAIDU_ALIGNMENT_1 = "/data/xlore20160223/Template/zhwiki-baidu-matched-property-1.dat"
ZHWIKI_BAIDU_ALIGNMENT_2 = "/data/xlore20160223/Template/zhwiki-baidu-matched-property-2.dat"
ZHWIKI_BAIDU_ALIGNMENT_3 = "/data/xlore20160223/Template/zhwiki-baidu-matched-property-3.dat"
ZHWIKI_BAIDU_ALIGNMENT_ALL = "/data/xlore20160223/Template/zhwiki-baidu-matched-property-all.dat"

"""
通过对齐的zhwiki与baidu的article，找出同一个article中对齐的property
"""

def similar(a, b):
    seta = set(re.findall(r'\d+', a))
    setb = set(re.findall(r'\d+', b))
    if len(seta) > 0 and len(setb) > 0:
        return len(seta&setb)*1.0 / len(seta|setb)
    #return SequenceMatcher(None, a, b).ratio()
    return Levenshtein.ratio(a,b)

def read_wiki_infobox(fn):
    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        if len(line.split('\t\t')) < 2:
            continue
        else:
            article, infos = line.strip('\n').split('\t\t')
            d[article] = {}
            new_infos = []
            for info in infos.split('\t'): #对每个template new_facts = {}
                tem, facts = info.split(':::::', 1)
                d[article][tem] = {}
                for fact in facts.split('::::;'):
                    if len(fact.split('::::=')) < 2:
                        continue
                    k, v = fact.split('::::=')
                    d[article][tem][k] = v
    return d

def find_aligned_attributes_1(baidufn, fo, zhwiki, all_matched):
    """
    同一实体的两百科词条中，信息框属性名称一致
    zhwiki: Template:property
    baidu : property
    """

    align_result = {}
    fw = codecs.open(fo, 'w', 'utf-8')

    for line in codecs.open(baidufn, 'r', 'utf-8'):
        if len(line.split('\t')) < 2:
            continue

        article, facts = line.strip('\n').split('\t')
        if not article in zhwiki: #该文章在zhwiki里没有，跳过
            continue

        for fact in facts.split('::;'):
            if len(fact.split(':::')) < 2: #不是k－v对的跳过
                continue

            k, v = fact.split(':::')
            for tem, infos in zhwiki[article].iteritems():
                if not tem in align_result:
                    align_result[tem] = set()

                for k1, v1 in infos.iteritems():
                    if k == k1 or k == label.clean_label(k1):
                        align_result[tem].add((k1, k))

    for tem, aligns in align_result.iteritems():
        all_matched[tem] = all_matched.get(tem, set()).union(aligns)

    logging.info('Method 1: Template Number: %d'%len(align_result))
    attr_num = 0
    for attrs in align_result.values():
       attr_num += len(attrs)
    logging.info('Method 1: Total aligned attrs: %d'%attr_num)

    for tem, attrs in align_result.iteritems():
        for zh, bai in attrs:
            fw.write("%s\t%s\t%s\n"%(tem, zh, bai))
            fw.flush()
    fw.close()

def find_aligned_attributes_2(baidufn, fo, zhwiki, all_matched):
    """
    同一实体的两百科词条中，信息框属性名称有相同字，属性值一样的
    """

    align_result = {}
    fw = codecs.open(fo, 'w', 'utf-8')

    for line in codecs.open(baidufn, 'r', 'utf-8'):
        if len(line.split('\t')) < 2:
            continue

        article, facts = line.strip('\n').split('\t')
        if not article in zhwiki: #该文章在zhwiki里没有，跳过
            continue

        for fact in facts.split('::;'):
            if len(fact.split(':::')) < 2: #不是k－v对的跳过
                continue

            k, v = fact.split(':::')
            for tem, infos in zhwiki[article].iteritems():
                if not tem in align_result:
                #    align_result[tem] = set()
                    align_result[tem] = {}

                for k1, v1 in infos.iteritems():
                    if k1 == 'image' or k1 == u'图像':
                        continue

                    if k == k1 or k == label.clean_label(k1):
                        continue

                    if len(v) > 0 and len(v1) > 0 and v == v1 and set(k)&set(k1): #属性名称有相同字，属性值一样
                        #align_result[tem].add((k1, k))
                        c = align_result[tem].get((k1, k), 0) + 1
                        align_result[tem][(k1, k)] = c

    logging.info('Method 2: Template Number: %d'%len(align_result))
    attr_num = 0
    for attrs in align_result.values():
       attr_num += len(attrs)
    logging.info('Method 2: Total aligned attrs: %d'%attr_num)

    #for tem, attrs in align_result.iteritems():
    #    for zh, bai in attrs:
    #        fw.write("%s\t%s\t%s\n"%(tem, zh, bai))
    #        fw.flush()
    #fw.close()

    attr_num = 0
    CONFIDENCE =2
    import copy
    for tem, attrs in copy.deepcopy(align_result).iteritems():
        for align, c in attrs.iteritems():
            if c > CONFIDENCE:
                attr_num += 1
                zh, bai = align
                fw.write("%s\t%s\t%s\n"%(tem, zh, bai))
                fw.flush()
            else:
                align_result[tem].pop(align)
    fw.close()

    for tem, aligns in align_result.iteritems():
        all_matched[tem] = all_matched.get(tem, set()).union(aligns)

    logging.info('Method 2: Aligned attrs after filter: %d'%attr_num)

def find_aligned_attributes_3(baidufn, fo, zhwiki, all_matched):
    """
    同一实体的两百科词条中，信息框属性值相似度高，且这一对出现次数大于3
    """

    SIMILAR = 0.6
    CONFIDENCE = 5

    logging.info('similar: %f\tconfidence: %d'%(SIMILAR, CONFIDENCE))

    align_result = {}
    fw = codecs.open(fo, 'w', 'utf-8')

    for line in codecs.open(baidufn, 'r', 'utf-8'):
        if len(line.split('\t')) < 2:
            continue

        article, facts = line.strip('\n').split('\t')
        if not article in zhwiki: #该文章在zhwiki里没有，跳过
            continue

        for fact in facts.split('::;'):
            if len(fact.split(':::')) < 2: #不是k－v对的跳过
                continue

            k, v = fact.split(':::')

            for tem, infos in zhwiki[article].iteritems():
                if not tem in align_result:
                    align_result[tem] = {}

                matched_zhwiki_key = set() #已经匹配的zhwiki property，我们认为一个zhwiki_property在一篇百度词条下只可能与一个百度属性对齐
                #for k1, v1 in infos.iteritems():

                #    if (k1, k) in align_result[tem]:
                #        matched_zhwiki_key.add(k1)

                for k1, v1 in infos.iteritems():
                    if k1 == 'image' or k1 == u'图像':
                        continue

                    if k1 in matched_zhwiki_key:
                        continue;

                    if tem in all_matched and (k1, k) in all_matched[tem]:
                        matched_zhwiki_key.add(k1)
                        continue

                    if similar(v, v1) > SIMILAR: #
                        c = align_result[tem].get((k1, k), 0) + 1
                        align_result[tem][(k1, k)] = c

    logging.info('Method 3: Template Number: %d'%len(align_result))
    attr_num = 0
    for attrs in align_result.values():
       attr_num += len(attrs)
    logging.info('Method 3: Total aligned attrs: %d'%attr_num)

    attr_num = 0
    import copy
    for tem, attrs in copy.deepcopy(align_result).iteritems():
        for align, c in attrs.iteritems():
            if c > CONFIDENCE:
                attr_num += 1
                zh, bai = align
                fw.write("%s\t%s\t%s\n"%(tem, zh, bai))
                fw.flush()
            else:
                align_result[tem].pop(align)
    fw.close()

    for tem, aligns in align_result.iteritems():
        all_matched[tem] = all_matched.get(tem, set()).union(aligns)

    logging.info('Method 3: Aligned attrs after filter: %d'%attr_num)

def merge(all_matched, fo):
    
    with codecs.open(fo, 'w', 'utf-8') as fw:
        for tem, matched in all_matched.iteritems():
            for zhwiki, baidu in sorted(matched):
                fw.write("%s\t%s\t%s\n"%(tem, zhwiki, baidu))
                fw.flush()

if __name__=='__main__':

    import time
    start = time.time()

    zhwiki = read_wiki_infobox(ZHWIKI_INFOBOX)
    all_matched = {}
    find_aligned_attributes_1(BAIDU_INFOBOX, ZHWIKI_BAIDU_ALIGNMENT_1, zhwiki, all_matched)
    find_aligned_attributes_2(BAIDU_INFOBOX, ZHWIKI_BAIDU_ALIGNMENT_2, zhwiki, all_matched)
    find_aligned_attributes_3(BAIDU_INFOBOX, ZHWIKI_BAIDU_ALIGNMENT_3, zhwiki, all_matched)
    merge(all_matched, ZHWIKI_BAIDU_ALIGNMENT_ALL)

    logging.info('Time Consuming:%f'%(time.time()-start))

