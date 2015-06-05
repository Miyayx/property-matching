# -*- coding:utf-8 -*-
import os
import re
import codecs

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl")
INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl")

O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl2")
O_INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl2")

LABEL_URI = {}
DATA_URI = {}
LABEL_DATA = {}

global COUNT
COUNT = None

def read_label_uri(fn, ofn):
    """ 
    Returns: d  dict  key:label, value:uri
    """
    print "read_label_uri"
    d = {}
    fw = open(ofn, 'w')
    global COUNT

    with open(fn, 'r') as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                l = line[line.index('"')+1: line.rindex('"')]
                d[l] = _id
                COUNT = _id #记录最后一个property的id，用来以后扩充用
                if is_label(l): #如果是label，放入labellist里
                    LABEL_URI[l] = _id
                    continue
                if is_data(l): #如果是data，与对应label uri放入字典里
                    DATA_URI[l] = _id
                    continue
            fw.write(line) #不是label或data的直接写入新文件
    fw.close()

    return d

def read_infobox(fn, ofn):
    print "read_infobox"
    prop_v_d = {}

    fw = open(ofn, 'w')
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                ins, prop, v = line.split(' ',2)
                _id = prop.split('/')[-1][:-1]
                if _id in LABEL_DATA.keys() or _id in LABEL_DATA.values(): #把带有label或data的infobox行提出来
                    if not ins in prop_v_d:
                        prop_v_d[ins] = {}
                    prop_v_d[ins][_id]=v
                    continue
            fw.write(line) #不需要替换的直接写入新文件
            fw.flush()
    fw.close()
                 
    return prop_v_d

def is_label(label):
    return True if re.match('^label'+'\d+$', label) else False

def is_data(label):
    return True if re.match('^data'+'\d+$', label) else False

def is_chinese(label):
    return True if re.match(ur'[\u4e00-\u9fff]+', label.decode('utf-8', 'ignore')) else False

if __name__ == "__main__":
    label_uri = read_label_uri(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL)
    print "labelx num:",len(LABEL_URI)
    print "datax num:",len(DATA_URI)
    
    for l, _id in DATA_URI.items():
        if l.replace('data','label') in LABEL_URI:
            LABEL_DATA[LABEL_URI[l.replace('data','label')]] = _id

    prop_v_d = read_infobox(INFOBOX_TTL, O_INFOBOX_TTL)#这里存的是 property uri和它的值
    
    new_prop_v = {} #这里存的是新的property labe和它的值
    #新的property lable和它的uri，如果新的在原property里有，就用原来的uri，否则编号加一创建一个新的property
    new_label_uri = {}

    COUNT = int(COUNT)
    print "COUNT:",COUNT
    
    print "create new uri for new labels"
    for ins, prop_v in prop_v_d.items():
        for label_id, v in prop_v.items():
            if label_id in LABEL_DATA:
                data_id = LABEL_DATA[label_id]
                try:
                    label = v[v.index('"')+1:v.rindex('"')]
                except:
                    continue
                if not data_id in prop_v:
                    continue
                value = prop_v[data_id]
                if not ins in new_prop_v:
                    new_prop_v[ins] = {}
                new_prop_v[ins][label] = value
                if label in label_uri:#如果原来的property有这个label，则用原来的uri
                    new_label_uri[label] = label_uri[label]
                else: #否则创建一个新的uri
                    COUNT += 1
                    new_label_uri[label] = str(COUNT)
                    
    print "new labels",len(new_label_uri)
    new_labels = set(new_label_uri.keys()) - set(label_uri.keys())#选出原来没有的label
    print "new labels",len(new_labels)

    with open(O_PROPERTY_LIST_TTL, 'a') as fw:
        #原来没有的加入property list
        #<7> rdf:type rdf:Property .
        #<13> rdfs:label "外文名"@zh .
        for l in new_labels:
            fw.write("<%s> rdf:type rdf:Property .\n"%new_label_uri[l])
            lan = "zh" if is_chinese(l) else "en"
            fw.write('<%s> rdfs:label "%s"@%s .\n'%(new_label_uri[l], l, lan))
            fw.flush()

    with open(O_INFOBOX_TTL, 'a') as fw:
        #使用新的uri，写入新的关系到infobox文件里
        for ins, prop_v in new_prop_v.items():
            for label, v in prop_v.items():
                fw.write("%s <http://xlore.org/property/%s> %s\n"%(ins, new_label_uri[label], v))
                fw.flush()
                    
