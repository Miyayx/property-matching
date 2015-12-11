
# -*- coding:utf-8 -*-

import re
import os
import codecs

from prop_io import *

#DIR = "/home/xlore/XloreData/etc/ttl/"
DIR = "/home/xlore/server36/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl2")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl2")

def property_use_stat(fn, propfn):
    s = set()
    multis = set()
    has_zero = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                #print line
                ins, prop, v = line.strip('\n').split(' ',2)
                p = prop[1:-1].split('/')[-1] 
                if p in s:
                    multis.add(p)
                else:
                    s.add(p)

    for line in open(propfn):
        if line.startswith('<'):
            _id = line[1:line.index('>')]
            #if _id in s:
            #    print "_id",_id
            if not _id in s:
                has_zero.add(_id)
    print "Total:",len(s)
    print "Multi:",len(multis)
    print "Has one:",len(s-multis)
    print "Has Zero:",len(has_zero)
    return (s - multis)^has_zero

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
    dels = property_use_stat(INFOBOX_TTL, PROPERTY_LIST_TTL)
    read_and_del(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL, dels)
    infobox_read_and_write2(INFOBOX_TTL, O_INFOBOX_TTL, dels)

