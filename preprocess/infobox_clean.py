# -*- coding:utf-8 -*-

"""
2. 没有value值的property丢弃
3. 删除带无用值（如图片）的property
4. 用render label 替代 template label
"""

import os,sys
import codecs
import re

ENWIKI_INFOBOX="/home/xlore/disk2/raw.wiki/enwiki-infobox-new.dat"
NEW_ENWIKI_INFOBOX="/home/xlore/server36/infobox/enwiki-infobox-new.dat"
ENWIKI_RENDER_LABEL="/home/xlore/server36/infobox/enwiki-template-triple.dat.uniq"

ZHWIKI_INFOBOX="/home/xlore/disk2/raw.wiki/zhwiki-infobox-new.dat"
NEW_ZHWIKI_INFOBOX="/home/xlore/server36/infobox/zhwiki-infobox-new.dat"
ZHWIKI_RENDER_LABEL="/home/xlore/server36/infobox/zhwiki-template-triple.dat.uniq"

def get_right_properties(fn):
    d = {}
    for line in open(fn):
        tem, temlabel, _, renlabel = line.strip('\n').split('\t')
        if not tem in d:
            d[tem] = {}
        d[tem][temlabel] = renlabel
    return d

def clean(fi, fo, templatefn):
    right_properties = get_right_properties(templatefn)

    fw = codecs.open(fo, 'w', 'utf-8')

    for line in codecs.open(fi, 'r', 'utf-8'):
        if len(line.split('\t\t')) < 2:
            fw.write(line)
        else:
            article, infos = line.strip('\n').split('\t\t')
            new_infos = []
            for info in infos.split('\t'): #对每个template new_facts = {}
                new_facts = []
                tem, facts = info.split(':::::', 1)
                for fact in facts.split('::::;'):
                    if len(fact.split('::::=')) < 2: #没有value的property
                        continue
                    k, v = fact.split('::::=')
                    if len(v) == 0: #没有value的property
                        print 'attr,',k,'has no value'
                        continue
                    if re.match(r'([-\w]+\.(?:jpg|gif|png))', v): #有图片
                        print 'image:',v
                        continue
                    if tem in right_properties and k in right_properties[tem]:
                        k = right_properties[tem][k]
                    new_facts.append(k+'::::='+v)
                new_infos.append(tem+':::::'+'::::;'.join(new_facts))

            fw.write('%s\t\t%s\n'%(article, '\t'.join(new_infos)))
            fw.flush()
    fw.close()

if __name__=="__main__":
    clean(ENWIKI_INFOBOX, NEW_ENWIKI_INFOBOX, ENWIKI_RENDER_LABEL)
    #clean(ZHWIKI_INFOBOX, NEW_ZHWIKI_INFOBOX, ZHWIKI_RENDER_LABEL)
