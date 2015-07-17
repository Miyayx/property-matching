# -*- coding:utf-8 -*-

"""
本模块程序负责：
    1. 合并重复编号的label
"""

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl3")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl3")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl4")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl4")

def read_label_uri2(fn, uri_labels):
    label_uri = {}
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                if l in label_uri:
                    if len(uri_labels[_id] == 2):#有双语的id优先
                        label_uri[l] = _id
                else:
                    label_uri[l] = _id
    return label_uri

def read_and_write(fn, ofn, label_uri):
    dup_count = 0
    del_uri = {} # deleted label to his mapping uri
    fw = codecs.open(ofn, 'w', 'utf-8')
    with codecs.open(fn,'r', 'utf-8') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                if not label_uri[l] == _id: #删除ttl中原本就重复的label，即如果l对应的uri和它本身的uri不一样，证明还有另一个label==l的label存在
                    dup_count += 1
                    del_uri[_id] = label_uri[l] #用label_uri里存储的uri代替多出来的uri
                    continue
            fw.write(line)
            fw.flush()
    fw.close()
    print "Delete duplidate num:%d"%(dup_count)
    return del_uri


if __name__=="__main__":
    uri_labels = read_uri_labels(PROPERTY_LIST_TTL)
    print "Reading label_uri"
    label_uri = read_label_uri2(PROPERTY_LIST_TTL)
    print "Reading and rewriting property list"
    del_uri = read_and_write(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL, label_uri)
    print "Reading and rewriting infobox"
    infobox_read_and_write(INFOBOX_TTL, O_INFOBOX_TTL, del_uri)
