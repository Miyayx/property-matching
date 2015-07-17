
# -*- coding:utf-8 -*-

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl2")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl2")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl3")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl3")

def property_use_stat(fn):
    s = set()
    multis = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                #print line
                ins, prop, v = line.strip('\n').split(' ',2)
                p = prop.split('/')[-1] 
                if p in s:
                    multis.add(p)
                else:
                    s.add(p)
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

def infobox_read_and_write2(fn, ofn, del_uris):
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn, 'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                ins, prop, v = line.split(' ',2)
                _id = prop.split('/')[-1][:-1]
                if _id in del_uris:
                    continue
            fw.write(line)
            fw.flush()
    fw.close()

if __name__ == "__main__":
    dels = property_use_stat(INFOBOX_TTL)
    read_and_write(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL, dels)
    infobox_read_and_write2(INFOBOX_TTL, O_INFOBOX_TTL, dels)

