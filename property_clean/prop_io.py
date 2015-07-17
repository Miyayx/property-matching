
# -*- coding:utf-8 -*-

import re
import os
import codecs

def read_label_uri(fn):
    label_uri = {}
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                if not l in label_uri:
                    label_uri[l] = _id
    return label_uri

def read_uri_labels(fn):
    uri_labels = {}
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                if not _id in uri_labels:
                    uri_labels[_id] = {}
                if "@en" in line:
                    uri_labels[_id]["en"] = l
                if "@zh" in line:
                    uri_labels[_id]["zh"] = l
    return uri_labels

def write_new_property_list(fn, uri_labels):
    with codecs.open(fn,'w', 'utf-8') as f:
        #<7> rdf:type rdf:Property .
        #<13> rdfs:label "外文名"@zh .
        for u, ls in sorted(uri_labels):
            f.write("<%s> rdf:type rdf:Property .\n"%str(u))
            if "en" in ls:
                f.write('<%s> rdfs:label "%s"@en .\n'%(str(u), ls["en"]))
            if "zh" in ls:
                f.write('<%s> rdfs:label "%s"@zh .\n'%(str(u), ls["zh"]))
            f.flush()

def infobox_read_and_write(fn, ofn, del_uris):
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn, 'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                ins, prop, v = line.split(' ',2)
                _id = prop.split('/')[-1][:-1]
                if _id in del_uris:
                    line = line.replace('xlore.org/property/%s'%_id, 'xlore.org/property/%s'%del_uris[_id])
            fw.write(line)
            fw.flush()
    fw.close()


