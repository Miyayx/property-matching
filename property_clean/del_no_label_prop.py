# -*- coding:utf-8 -*-

import re
import os
import codecs

from prop_io import *

DIR = "/home/xlore/XloreData/etc/ttl/"
PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl7")
O_PROPERTY_LIST_TTL = os.path.join(DIR, "xlore.property.list.ttl8")

def find_no_label(fn):
    s = set()
    multis = set()
    with open(fn) as f:
        for line in f:
            if line.startswith('<'):
                _id = line.split(' ',1)[0][1:-1]
                if _id in s:
                    multis.add(_id)
                else:
                    s.add(_id)
    return s - multis 

if __name__ == "__main__":
    dels = find_no_label(PROPERTY_LIST_TTL)
    read_and_del(PROPERTY_LIST_TTL, O_PROPERTY_LIST_TTL, dels)

