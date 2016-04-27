# -*- coding:utf-8 -*-
import os

DIR = "/Users/Miyayx/server36/infobox"
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-template-triple.dat.uniq.bak")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-template-triple.dat.uniq.bak")
MATCHED_TEMPLATE = "../data/template.cl"

MATCHED_TEMPLATE_LABEL = os.path.join(DIR, "matched-template-label.dat")

enwiki = {}

m_tem = {}

import re

def remove_square(s):
    if '[[' in s and ']]' in s:
        for i in re.findall(r"\[\[(.*?)\]\]",s):
            if '|' in i:
                return i.split('|')[0]
            else:
                return i
    else:
        return s

for line in open(MATCHED_TEMPLATE):
    en, zh = line.strip('\n').split('\t')
    m_tem[zh] = en

fw = open(MATCHED_TEMPLATE_LABEL, 'w')

with open(ENWIKI_TEMPLATE_LABEL) as fe:
    for line in fe:
        #print line
        tem, endl, zhdl, pl = line.strip('\n').split('\t')
        if not tem in enwiki:
            enwiki[tem] = {}
        enwiki[tem][endl] = pl

with open(ZHWIKI_TEMPLATE_LABEL) as fz:
    for line in fz:
        tem, endl, zhdl, pl = line.strip('\n').split('\t') 
        if not tem in m_tem:
            print "Template %s key error"%tem
            continue
        en_tem = m_tem[tem]
        if en_tem in enwiki:
            if endl in enwiki[en_tem]:
                fw.write('%s\t%s\n'%(remove_square(pl), remove_square(enwiki[en_tem][endl])))
                fw.flush()
fw.close()

