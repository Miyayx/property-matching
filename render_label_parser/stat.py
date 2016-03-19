# -*- coding:utf-8 -*-

def notuse_template(all_t_fn, used_t_fn, extracted_t_fn):
    all_t = set([line.strip('\n') for line in open(all_t_fn)])
    used_t = set(['Template:'+line.strip('\n') for line in open(used_t_fn)])
    extracted_t = set([line.strip('\n').split('\t')[0] for line in open(extracted_t_fn) if len(line.split('\t')) > 1])
    
    common = all_t & used_t
    not_used = all_t - used_t
    used_but_not_in_list = used_t - all_t
    used_but_not_extracted = used_t - extracted_t

    print "Common:", len(common)
    print "Used", len(used_t)
    print "Not used", len(not_used)
    print "Used but not in list", len(used_but_not_in_list)
    print "Extracted", len(extracted_t)
    print "Used but not extracted", len(used_but_not_extracted)
    for t in sorted(used_but_not_extracted):
        print t

def previous_compare(previous_fn, curr_fn):
    prev_t = set([line.split('\t')[0] for line in open(previous_fn)])
    curr_t = set([line.split('\t')[0] for line in open(curr_fn) if len(line.split('\t')) > 1])

    for t in sorted(prev_t-curr_t):
        print t

    print "Previous Templates",len(prev_t)
    print "Current Templates", len(curr_t)
    print "Previous templates not extract this time", len(prev_t - curr_t)
    print "new extracted ones", len(curr_t - prev_t)

if __name__=="__main__":
    #notuse_template("/data/xlore20160223/wikiExtractResult/zhwiki-template-name.dat", "/data/xlore20160223/Template/zhwiki-infobox-template.dat", "/data/xlore20160223/Template/zhwiki-20160203-template-triple.dat" )
    previous_compare("/data/xlore20160223/Template/old/zhwiki-template-triple.dat.uniq", "/data/xlore20160223/Template/zhwiki-20160203-template-triple.dat")

    


