# -*- coding:utf-8 -*-

import codecs
import sys
import copy
sys.path.append('..')
from utils.logger import *
initialize_logger('./coverage.log')
from fileio import *

def template_replace(a_tem, tem_redirect, tems):
    """
    用标准template替代抽取出的不规则template命名
    """
    a_tem2 = copy.copy(a_tem)
    for a, tem in a_tem2.iteritems():
        ntem = tem.strip().replace('_',' ')
        if ntem in tem_redirect:
            ntem = tem_redirect[ntem]
        if ntem in tems:
            a_tem[a] = ntem  #修改一下抽取出来的不规则的template命名
            print tem,'-->',ntem
    return a_tem

def article_coverage(tem_triple, a_tem, tem_redirect):
    count = 0
    tems = tem_triple.keys()
    for tem in a_tem.values():
        if tem in tems:
            count += 1

    logging.info("Articles: %d"%len(a_tem.keys()))
    logging.info("Hit: %d"%count)
    logging.info("Article coverage: %f\n"%(count*1.0/len(a_tem.values())))

def template_coverage(tem_triple, a_tem, tem_redirect):
    tems = tem_triple.keys()
    infobox_tems = set()
    not_cover = set()
    fw = codecs.open(WIKI+'-not_cover_template.dat', 'w', 'utf-8')
    for tem in a_tem.values():
        if tem in tems:
            infobox_tems.add(tem)
        else:
            not_cover.add(tem)

    for t in sorted(not_cover):
        fw.write(t+'\n')
    fw.close()

    s = len(infobox_tems)+len(not_cover)
    hit = len(infobox_tems)
    logging.info("wiki-infobox Template: %d"%(s))
    logging.info("Parsed Infobox Template: %d"%(len(tems)))
    logging.info("Hit: %d"%hit)
    logging.info("Template coverage: %f\n"%(hit*1.0/s))

def infobox_coverage(tem_triple, a_tem, a_infobox):

    tem_attribute = {}
    for a, infobox in a_infobox.iteritems():
        tem = a_tem[a]
        if not tem in tem_attribute:
            tem_attribute[tem] = set()
        for k in infobox:
            tem_attribute[tem].add(k)

    total = hit = 0
    for tem, attrs in tem_attribute.iteritems():
        total += len(attrs)
        if tem in tem_triple:
            for a in attrs:
                if a in tem_triple[tem]:
                    hit += 1

    logging.info("Total: %d"%total)
    logging.info("Hit: %d"%hit)
    logging.info("Infobox coverage: %f\n"%(hit*1.0/total))

def infobox_replace(tem_triple, a_tem, a_infobox):
    pass
    

if __name__=="__main__":
    import time
    start = time.time()

    DIR = "/data/xlore20160223"
    global WIKI
    WIKI = "zhwiki"

    #tem_triple = read_template_triple(os.path.join(DIR, "Template/enwiki-20160305-template-triple.dat"))
    #tem_triple.update(read_template_triple(os.path.join(DIR, "Template/enwiki-20160305-inherit-template-triple.dat")))
    #tem_redirect = read_redirect_template(os.path.join(DIR, "Template/enwiki-template-redirect.dat"))
    #a_tem, a_infobox = read_wiki_infobox(os.path.join(DIR, "wikiExtractResult/enwiki-infobox-tmp.dat"))

    tem_triple = read_template_triple(os.path.join(DIR, "Template/zhwiki-20160203-template-triple.dat"))
    tem_triple.update(read_template_triple(os.path.join(DIR, "Template/zhwiki-20160203-inherit-template-triple.dat")))
    tem_redirect = read_redirect_template(os.path.join(DIR, "Template/zhwiki-template-redirect.dat"))
    a_tem, a_infobox = read_wiki_infobox(os.path.join(DIR, "wikiExtractResult/zhwiki-infobox-tmp.dat"))

    a_tem = template_replace(a_tem, tem_redirect, a_tem.values())
    template_coverage(tem_triple, a_tem, tem_redirect)
    infobox_coverage(tem_triple, a_tem, a_infobox)
    article_coverage(tem_triple, a_tem, a_infobox)

    print 'Time Consuming:',time.time()-start
    
