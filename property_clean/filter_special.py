# -*- coding:utf-8 -*-

"""
本模块程序负责：
    1. 删除label中的特殊字符，并把清理后的label与相同的已存在label合并
    2. 合并重复编号的label
"""

import re
import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl3")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl3")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl4")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl4")

def filter_special(label):
    #return label.strip('*').strip('-').strip('·').strip('，').strip('：').rstrip('(').strip('：').strip('，').strip(u'\u200b').strip()
    return label.strip(u'*').strip(u'-').strip(u'·').strip(u'：').rstrip(u'(').strip(u'，').strip(u'\u200b').strip()

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

def read_and_write(fn, ofn, label_uri):
    count = 0 
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
                l2 = filter_special(l)
                if not l == l2: #清洗后发现前后label不一样，证明原label是有特殊符号的。
                    print "%s --> %s"%(l, l2) 
                    count += 1
                    if l2 in label_uri:#这时如果新label已存在在label列表里，则用已有label的uri代替原label的uri。
                        del_uri[_id] = label_uri[l2]
                        continue
                    else:#如果不存在就用新label字符串代替原label字符串
                        line = line.replace(l, l2)
            fw.write(line)
            fw.flush()
    fw.close()
    print "Delete duplidate num:%d"%(dup_count)
    print "Filter num:%d"%(count)
    return del_uri

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

if __name__=="__main__":
    print "Reading label_uri"
    label_uri = read_label_uri(PROPERTY_LIST_TTL)
    print "Reading and rewriting property list"
    del_uri = read_and_write(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL, label_uri)
    print "Reading and rewriting infobox"
    infobox_read_and_write(INFOBOX_TTL, O_INFOBOX_TTL, del_uri)

