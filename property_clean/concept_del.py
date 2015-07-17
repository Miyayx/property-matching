
# -*- coding:utf-8 -*-

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
CONCEPT_LIST_TTL = os.path.join(DIR, "xlore.concept.list.ttl")
TAXONOMY_TTL = os.path.join(DIR, "xlore.taxonomy.ttl")
O_CONCEPT_LIST_TTL = os.path.join(DIR, "xlore.concept.list.ttl2")
O_TAXONOMY_TTL = os.path.join(DIR, "xlore.taxonomy.ttl2")

def concept_stat(fn):
    s = set()
    multis = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/concept/' in line and 'xlore.org/instance/':
                con, ins = line.strip('\n').split(' ',1)
                c = con.split('/')[-1] 
                if c in s:
                    multis.add(c)
                else:
                    s.add(c)
    return s - multis 


def read_and_write(fn, ofn, del_uris):
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                if _id in del_uris:
                    continue
            fw.write(line)
            fw.flush()
    fw.close()

def taxonomy_read_and_write2(fn, ofn, del_uris):
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn, 'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/concept/' in line:
                sup, sub = line.split(' ',1)
                _id = sup.split('/')[-1]
                if _id in del_uris:
                    continue
                if 'concept' in sub:
                    _id = sub.split('/')[-1]
                    if _id in del_uris:
                        continue
            fw.write(line)
            fw.flush()
    fw.close()

if __name__ == "__main__":
    dels = concept_stat(TAXONOMY_TTL)
    read_and_write(CONCEPT_LIST_TTL, O_CONCEPT_LIST_TTL, dels)
    taxonomy_read_and_write2(TAXONOMY_TTL, O_TAXONOMY_TTL, dels)

