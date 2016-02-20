#-*- coding:utf-8 -*-

import sys,os,re
import codecs

from utils import *

def enwiki_value(fi, fo):
    queries = set()
    fw = codecs.open(fo, 'w', 'utf-8')
    for line in codecs.open(fi, 'r', 'utf-8'):
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
                    if not_translate(k, v):
                        continue
                    queries.add(v)
    for q in queries:
        fw.write(q+'\n')
    fw.close()
    
def baidu_value(fi, fo):
    queries = set()
    fw = codecs.open(fo, 'w', 'utf-8')
    for line in codecs.open(fi, 'r','utf-8'):
        try:
            title, info = line.strip('\n').split('\t')
        except:
            continue
        for item in info.split('::;'):
            try:
                k, v = item.split(':::')
            except:
                continue
            queries.add(v)
    for q in queries:
        fw.write(q+'\n')
    fw.close()
    

if __name__=="__main__":
    if len(sys.argv) < 3:  
       print 'No input and output files'  
       sys.exit()  

    fi, fo = sys.argv[1], sys.argv[2]
    #enwiki_value(fi, fo)
    baidu_value(fi, fo)


