# -*- coding:utf-8 -*-

import re
import os
import codecs

"""
删除只有一个或没有instance/concept的concept
"""

#DIR = "/home/xlore/XloreData/etc/ttl/"
DIR = "/home/xlore/server36/ttl/"
CONCEPT_LIST_TTL = os.path.join(DIR, "xlore.concept.list.ttl")
TAXONOMY_TTL = os.path.join(DIR, "xlore.taxonomy.ttl")
O_CONCEPT_LIST_TTL = os.path.join(DIR, "xlore.concept.list.ttl2")
O_TAXONOMY_TTL = os.path.join(DIR, "xlore.taxonomy.ttl2")


def concept_stat(fn, confn):
    #<http://xlore.org/instance/1422347> <http://xlore.org/property#isRelatedTo> <http://xlore.org/concept/4563> .
    #<http://xlore.org/instance/6480808> owl:InstanceOf <http://xlore.org/concept/9276> .
    s = set()
    multis = set()
    has_zero = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and not 'rdf' in line:
                sub, rel, sup = line.strip('\n').split()[:3]
                c = sup[1:-1].split('/')[-1] 
                if c in s:
                    multis.add(c)
                else:
                    s.add(c)

    for line in open(confn):
        if line.startswith('<'):
            _id = line[1:line.index('>')]
            #if _id in s:
            #    print "_id",_id
            if not _id in s:
                has_zero.add(_id)
    print "Total:",len(s)
    print "Multi:",len(multis)
    print "Has one:",len(s-multis)
    #for o in s-multis:
    #    print "ones",o
    print "Has Zero:",len(has_zero)
    #for z in has_zero:
    #    print "zero:",z
    return (s - multis)^has_zero

def concept_not_in_taxonomy(fn, confn):
    s = set()
    not_in = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and not 'rdf' in line:
                sub, rel, sup = line.strip('\n').split()[:3]
                c = sup[1:-1].split('/')[-1] 
                s.add(c)
                if "concept" in sub:
                    c2 = sub[1:-1].split('/')[-1] 
                    s.add(c2)

    for line in open(confn):
        if line.startswith('<'):
            _id = line[1:line.index('>')]
            #if _id in s:
            #    print "_id",_id
            if not _id in s:
                not_in.add(_id)
    print "Total:",len(s)
    print "Not in",len(not_in)
    return not_in

def read_and_write(fn, ofn, del_uris):
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<'):
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
                sub, rel, sup = line.split()[:3]
                _id = sup[1:-1].split('/')[-1] 
                if _id in del_uris:
                    continue
                if 'concept' in sub:
                    _id = sub[1:-1].split('/')[-1] 
                    if _id in del_uris:
                        continue
            fw.write(line)
            fw.flush()
    fw.close()

if __name__ == "__main__":
    ### 删除没有或只有一个instance/concept 的concept
    #dels = concept_stat(TAXONOMY_TTL, CONCEPT_LIST_TTL)
    #print "Delete %d concepts"%(len(dels))
    #read_and_write(CONCEPT_LIST_TTL, O_CONCEPT_LIST_TTL, dels)
    #taxonomy_read_and_write2(TAXONOMY_TTL, O_TAXONOMY_TTL, dels)

    ### 只删除未在taxonomy中出现的
    dels = concept_not_in_taxonomy(TAXONOMY_TTL, CONCEPT_LIST_TTL)
    print "Delete %d concepts"%(len(dels))

