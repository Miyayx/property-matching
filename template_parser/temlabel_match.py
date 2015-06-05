# -*- coding:utf-8 -*-
import os

DIR = "/mnt/lmy_36/infobox"
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-template-triple.dat")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-template-triple.dat")

MATCHED_TEMPLATE_LABEL = os.path.join(DIR, "matched-template-label.dat")

enwiki = {}

fw = open(MATCHED_TEMPLATE_LABEL, 'w')

with open(ENWIKI_TEMPLATE_LABEL) as fe:
    for line in fe:
        print line
        endl, pl = line.split('\t')[:2] 
        enwiki[endl.lower()] = pl

with open(ZHWIKI_TEMPLATE_LABEL) as fz:
    for line in fz:
        zhdl, pl = line.split('\t')[:2] 
        k = zhdl.lower()
        if k in enwiki:
            fw.write('%s\t%s\t%s\n'%(k, pl, enwiki[k]))
            fw.flush()
fw.close()

