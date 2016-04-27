#-*- coding:utf-8 -*-
import os

DIR = '/Users/Miyayx/server36'
FILES = ['baikedump/baidu-dump-20150702.dat', 'baikedump/hudong-dump-20150702.dat']
OUTPUT = 'word2vec/prop_names'

fw = open(os.path.join(DIR, OUTPUT), 'w')

for fn in FILES:
    fn = os.path.join(DIR, fn)
    for line in open(fn):
        if line.startswith('Infoboxes:'):
            items = []
            line = line[len('Infoboxes:'):]
            pairs = line.split('::;')
            for p in pairs:
                #items += p.split('::=')
                items.append(p.split('::=')[0])
            fw.write(' '.join(items))
            fw.flush()
fw.close()
            



