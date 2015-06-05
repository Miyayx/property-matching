# -*- coding:utf-8 -*-

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl2")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl2")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl3")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl3")

def is_special(label):
    special = ['header']
    for sp in special:
        if re.match(sp+'\d+', label):
            return True
    return False

def is_short_or_long(label):
    if re.match(ur'[\u4e00-\u9fff]+', label.decode('utf-8', 'ignore')):
        #print "chinese",label
        if len(label) > 30:
            print "zh",label
            return True
        if len(label) == 1:
            print "1",label
            return True
    else:
        if len(label.split()) > 6:
            print "6 words",label
            return True
        #if re.match(label, '\w'):
        if len(label) == 1:
            print "1",label
            return True
    return False

def read_and_write(fn, ofn):
    del_uri = []
    fw = open(ofn, 'w')
    with open(fn,'r') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                if is_short_or_long(l) or is_special(l):
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

if __name__ == "__main__":
    del_uris = read_and_write(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL)
    print "del labels:",len(del_uris)
    infobox_read_and_write(INFOBOX_TTL, O_INFOBOX_TTL, del_uris)
