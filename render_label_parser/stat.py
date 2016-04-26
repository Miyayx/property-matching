# -*- coding:utf-8 -*-

import sys
sys.path.append('..')
from utils.logger import *
initialize_logger('./stat.log')

def notuse_template(all_t_fn, used_t_fn, extracted_t_fn):
    all_t = set([line.strip('\n') for line in open(all_t_fn)])
    used_t = set(['Template:'+line.strip('\n') for line in open(used_t_fn)])
    extracted_t = set([line.strip('\n').split('\t')[0] for line in open(extracted_t_fn) if len(line.split('\t')) > 1])
    
    common = all_t & used_t
    not_used = all_t - used_t
    used_but_not_in_list = used_t - all_t
    used_but_not_extracted = used_t - extracted_t

    logging.info("Common: %d"%len(common))
    logging.info("Used: %d"%len(used_t))
    logging.info("Not used : %d"%len(not_used))
    logging.info("Used but not in list: %d"%len(used_but_not_in_list))
    logging.info("Extracted %s"%len(extracted_t))
    logging.info("Used but not extracted %d\n"%len(used_but_not_extracted))
    #for t in sorted(used_but_not_extracted):
    #    print t

def previous_compare(previous_fn, curr_fn, redirect_fn):
    prev_t = set([line.split('\t')[0] for line in open(previous_fn)])
    curr_t = set([line.split('\t')[0] for line in open(curr_fn) if len(line.split('\t')) > 1])
    redirect_t = dict((line.strip('\n').split('\t')) for line in open(redirect_fn))
    redirect_curr_t = set()
    redirect_n = 0

    for t in sorted(prev_t-curr_t):
        if t in redirect_t and redirect_t[t] in curr_t:
            redirect_n += 1
            redirect_curr_t.add(redirect_t[t])
        else:
            print t

    logging.info("Previous Templates %d"%len(prev_t))
    logging.info("Current Templates: %d"%len(curr_t))
    logging.info("Redirect Templates: %d"%redirect_n)
    logging.info("Previous templates not extract this time: %d"%(len(prev_t - curr_t) - redirect_n))
    logging.info("new extracted ones %d\n"%len(curr_t - prev_t - redirect_curr_t))

if __name__=="__main__":
    #notuse_template("/data/xlore20160223/wikiExtractResult/zhwiki-template-name.dat", "/data/xlore20160223/Template/zhwiki-infobox-template.dat", "/data/xlore20160223/Template/zhwiki-20160203-template-triple.dat" )
    #previous_compare("/data/xlore20160223/Template/old/zhwiki-template-triple.dat.uniq", "/data/xlore20160223/Template/zhwiki-20160203-template-triple.dat", "/data/xlore20160223/Template/zhwiki-template-redirect.dat")
    #notuse_template("/data/xlore20160223/wikiExtractResult/enwiki-template-name.dat", "/data/xlore20160223/Template/enwiki-infobox-template.dat", "/data/xlore20160223/Template/enwiki-20160305-template-triple.dat" )
    previous_compare("/data/xlore20160223/Template/old/enwiki-template-triple.dat.uniq", "/data/xlore20160223/Template/enwiki-20160305-template-triple.dat", "/data/xlore20160223/Template/enwiki-template-redirect.dat")

    
