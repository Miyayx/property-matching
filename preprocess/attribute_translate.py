#-*- coding:utf-8 -*-

import sys
import codecs
from infobox_translate import Translater

def read_all_attributes(fn):
    attrs = {}
    count = 0
    for line in codecs.open(fn, 'r', 'utf-8'):
        count += 1
        #if count > 10000:
        #    break
        if len(line.split('\t\t')) < 2:
            continue
        else:
            article, infos = line.strip('\n').split('\t\t')
            new_infos = []
            for info in infos.split('\t'):
                tem, facts = info.split(':::::', 1)
                for fact in facts.split('::::;'):
                    if len(fact.split('::::=')) < 2:
                        continue
                    k, v = fact.split('::::=')
                    attrs[k] = ""
    return attrs

def read_all_baiduattributes(fn):
    attrs = {}
    count = 0
    for line in codecs.open(fn, 'r', 'utf-8'):
        count += 1
        #if count > 10000:
        #    break
        if len(line.split('\t')) < 2:
            continue
        else:
            article, facts = line.strip('\n').split('\t')
            for fact in facts.split('::;'):
                if len(fact.split(':::')) < 2:
                    continue
                try:
                    k, v = fact.split(':::')
                    attrs[k] = ""
                except:
                    #print fact
                    pass
    return attrs

def translate(attrs):
    attrs = attrs.keys()
    translater = Translater()
    n = 500
    i = 0
    while n*i < len(attrs):
        res = translater.translate('\n'.join(attrs[n*i:n*(i+1)]), 'zh', 'en')
        for k, v in res.iteritems():
            print '%s\t%s'%(k.encode('utf-8'),v.encode('utf-8'))
        i += 1
    

if __name__=="__main__":
    if len(sys.argv) < 2:  
       print 'No input file'  
       sys.exit()  

    fi = sys.argv[1]
    #attrs = read_all_attributes(fi)
    attrs = read_all_baiduattributes(fi)
    print 'Total attrs:',len(attrs)
    translate(attrs)
