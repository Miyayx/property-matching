# -*- coding:utf-8 -*-

import re

def is_special(label):
    special = ['header','label','data']
    for sp in special:
        if re.match(sp+'\d+'):
            return True
    return False

def is_short_or_long(label):
    if len(label) > 10:
        return True
    #if re.match(label, '\w'):
    if len(label) == 1:
        return True
    return False

def del_special(label):
    label = label.strip('*').strip('-').strip()

def read_uri_label(fn):
    d = {}
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'rdfs:label' in line:
                _id = line[1:line.index('>')]
                label_lan = line.spilt()[2]
                l, lan = label_lan.rsplit('@',1)
                l = l[1:-1]

                labeld = d.get(_id,{})
                labeld[lan] = l
                d[_id] = labeld
    return d

def property_use_stat(fn):
    d = {}
    with open(fn) as f:
        if line.startswith('<') and 'xlore.org/property/' in line:
            ins, prop, v = line.strip('\n').split()
            d[prop] = d.get(prop, 0) + 1
    return d

if __name__ == "__main__":
    DIR = "/home/xlore/XLoreData/etc/ttl/"
    PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl")
    INFOBOX_TTL = os.path.join(DIR, "xlore.instance.infobox.ttl")
    d = read_uri_label(PROPERTY_LIST_TTL)
    print "Initial %d"%len(d)
    for k,v in d.items():
        for k1, v1 in v.items():
            if is_short_or_long(v1):
                del v[k1]
            elif is_special(v1):
                del v[k1]
            else:
                v1 = del_special(v1)
                d[k][k1] = v1
        if len(d[k]) == 0:
            del d[k]
    stat = property_use_stat(INFOBOX_TTL)
    for k,v in stat.items():
        if v == 1:
            _id = k.split('/')[-1]
            print k
            del d[_id]

    print "Now %d"%len(d)
