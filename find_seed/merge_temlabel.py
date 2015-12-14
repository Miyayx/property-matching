
# -*- coding:utf-8 -*-
import os

"""
把爬取获得的英文模版，重复的合并。如删除/sandbox, 不区分大小写单词
"""

DIR = "/home/keg/data/infobox"
ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "enwiki-template-triple.dat.uniq")
ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "zhwiki-template-triple.dat.uniq")
NEW_ENWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-enwiki-template-triple.dat.uniq")
NEW_ZHWIKI_TEMPLATE_LABEL = os.path.join(DIR, "new-zhwiki-template-triple.dat.uniq")

def merge_similar_tem(tem):
    """
    Find the similar tempaltes and merge them into one
    """
    
    tem_label = {}
    new_tem = {}
    for t, d in tem.iteritems():
        label = t
        if '/sandbox' in label:
            label = t.rsplit('/',1)[0]
        tem_label[t] = label
        if not label in new_tem:
            new_tem[label] = set()
        new_tem[label] = new_tem[label].union(d)
    return tem_label, new_tem

def read_tem(fn):
    tem = {}
    for line in open(fn):
        t, l = line.split('\t', 1)
        if not t in tem:
            tem[t] = set()
        tem[t].add(l)
    return tem

def write_to_file(tem, fn):
    with open(fn, 'w') as f:
        for t, s in sorted(tem.items()):
            for line in sorted(s):
                f.write(t+'\t'+line)
                f.flush()

if __name__ == '__main__':
    en_tem = read_tem(ENWIKI_TEMPLATE_LABEL)
    en_tem_label, new_en_tem = merge_similar_tem(en_tem)
    write_to_file(new_en_tem, NEW_ENWIKI_TEMPLATE_LABEL)

    zh_tem = read_tem(ZHWIKI_TEMPLATE_LABEL)
    zh_tem_label, new_zh_tem = merge_similar_tem(zh_tem)
    write_to_file(new_zh_tem, NEW_ZHWIKI_TEMPLATE_LABEL)


