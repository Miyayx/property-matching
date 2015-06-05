
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
    d = {}
    with open(fn) as f:
        for line in f:
            if line.startswith('<') and 'xlore.org/property/' in line:
                #print line
                ins, prop, v = line.strip('\n').split(' ',2)
                d[prop] = d.get(prop, 0) + 1
    return d
