# -*- coding:utf-8 -*-

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl3")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl3")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl4")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl4")

def filter_special(label):
    return label.strip('*').strip('-').strip('·').strip('，').strip('：').rstrip('(').strip('：').strip('，').strip(u'\u200b').strip()

def read_label_uri(fn):
    label_uri = {}
    with open(fn,'r') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                label_uri[l] = _id
    return label_uri

def read_and_write(fn, ofn):
    del_uri = []
    fw = open(ofn, 'w')
    with open(fn,'r') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                l2 = filter_special(l)
                if not l == l2:
                    del_uri.append(_id)
                    continue
            fw.write(line)
            fw.flush()
    fw.close()
    return del_uri

def infobox_read_and_write(fn, ofn, del_uris):
    fw = open(ofn, 'w')
    with open(fn,'r') as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                ins, prop, v = line.split(' ',2)
                _id = prop.split('/')[-1][:-1]
                if _id in del_uris:
                    continue
            fw.write(line)
            fw.flush()
    fw.close()

if __name__=="__main__":


