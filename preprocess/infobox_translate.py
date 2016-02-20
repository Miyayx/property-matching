#-*- coding:utf-8 -*-

import sys,os,re
import codecs

from utils import *
from baidu_vip_translater import BaiduTranslater
from baidu_translater import Translater

def start(fi, fo):
    
    #translater = Translater()
    translater = BaiduTranslater()
    fw = codecs.open(fo, 'w', 'utf-8')
    i = 0
    for line in codecs.open(fi, 'r', 'utf-8'):
        i += 1
        if len(line.split('\t\t')) < 2:
            fw.write(line)
        else:
            article, infos = line.strip('\n').split('\t\t')
            new_infos = []
            for info in infos.split('\t'):
                tem, facts = info.split(':::::', 1)
                queries = []
                for fact in facts.split('::::;'):
                    if len(fact.split('::::=')) < 2:
                        continue
                    k, v = fact.split('::::=')
                    if not_translate(k, v):
                        continue
                    queries.append(v)
                res = translater.translate('\n'.join(queries))
                for k, v in res.iteritems():
                    #print 'replace',k,'to',v
                    info = info.replace(k ,v)
                    #print 'new line:',info
                new_infos.append(tem+':::::'+info)
                print i, info
            fw.write('%s\t\t%s\n'%(article, '\t'.join(new_infos)))
            fw.flush()
    fw.close()

def label_translate(fi, fo, d={}):
    print 'Have translated:', len(d)
    translater = BaiduTranslater()
    fw = codecs.open(fo, 'w', 'utf-8')
    queries = []
    try:
        for line in codecs.open(fi, 'r', 'utf-8'):
            #if i > 300:
            #    break
            q = line.strip('\n').replace('_', ' ')
            if q in d:
                continue
            queries.append(q)
            if (len(queries) >= 100):
                res = translater.translate('\n'.join(queries))
                print res
                d.update(res)
                print "d lenght:",len(d)
                queries = []
        res = translater.translate('\n'.join(queries))
        d.update(res)
    except Exception,e:
        print e

    for t in sorted(d.iteritems(), key=lambda v: v[0]):
        fw.write(t[0]+'\t'+t[1]+'\n')
    fw.close()

def load_dict(fi):
    return dict((line.strip('\n').split('\t')) for line in codecs.open(fi, 'r', 'utf-8'))

if __name__=="__main__":
    if len(sys.argv) < 3:  
       print 'No input and output files'  
       sys.exit()  

    fi, fo = sys.argv[1], sys.argv[2]
    #start(fi, fo)
    d = load_dict(sys.argv[2])
    label_translate(fi, fo, d)

  
