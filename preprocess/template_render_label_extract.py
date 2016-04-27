#-*- coding:utf-8 -*-

import sys,os,re
import codecs

from utils import *

def render_label(fi, fo):
    queries = set()
    fw = codecs.open(fo, 'w', 'utf-8')
    for line in codecs.open(fi, 'r','utf-8'):
        try:
            tem, tl, rl = line.strip('\n').split('\t')[:3]
            if re.match(r'\[\[.*?\]\]', rl):
                label = re.findall(r"\[\[.*?\]\]", rl)[0]
                inlabel =re.findall(r"\[\[(.*?)\]\]", rl)[0] 
                label = rl.replace(label, inlabel.split('|')[-1])
                queries.add(label)
            elif re.search(r'\d+', rl):
                continue
            else:
                queries.add(rl)
        except Exception,e:
            print e
            print line

    for q in sorted(queries):
        fw.write(q+'\n')
    fw.close()

if __name__=="__main__":
    if len(sys.argv) < 3:  
       print 'No input and output files'  
       sys.exit()  

    fi, fo = sys.argv[1], sys.argv[2]
    render_label(fi, fo)
