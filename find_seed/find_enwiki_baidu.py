# -*- coding:utf-8 -*-
import os,codecs

DIR = "/data/xlore20160223/Template"
ENWIKI_ZHWIKI = os.path.join(DIR, "matched-template-label-all-2.dat")
#ENWIKI_ZHWIKI = os.path.join(DIR, "enwiki-zhwiki-matched-property-all.dat")
ZHWIKI_BAIDU  = os.path.join(DIR, "zhwiki-baidu-matched-property-all.dat")
ENWIKI_BAIDU  = os.path.join(DIR, "enwiki-baidu-matched-property-all.dat")

def find_enwiki_baidu(enwiki_zhwiki, zhwiki_baidu, fo):
    """
    enwiki_zhwiki: 
        k: entem \t enlabel
        v: zhtem and zhlabel list

    zhwiki_baidu:
        k: zhtem \t zhlabel
        v: baidu label list
    """

    fw = codecs.open(fo, 'w', 'utf-8')
    for enwiki, zhwikis in sorted(enwiki_zhwiki.items()):
        for zhwiki in zhwikis:
            if zhwiki in zhwiki_baidu:
                for b in zhwiki_baidu[zhwiki]:
                    fw.write(enwiki+'\t'+b+'\n')

def read_enwiki_zhwiki(fn):

    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        enwiki, zhwiki = line.strip('\n').split('\t')
        enwiki = enwiki.replace('###', '\t')
        zhwiki = zhwiki.replace('###', '\t')
        if not enwiki in d:
            d[enwiki] = []
        d[enwiki].append(zhwiki)

    #for line in codecs.open(fn, 'r', 'utf-8'):
    #    enwiki, zhwiki = line.strip('\n').split('\t\t')
    #    e1, e2 = enwiki.split('@@')
    #    z1, z2 = enwiki.split('@@')
    #    enwiki = e2+'\t'+e1
    #    zhwiki = z2+'\t'+z1

    #    if not enwiki in d:
    #        d[enwiki] = []
    #    d[enwiki].append(zhwiki)
    return d

def read_zhwiki_baidu(fn):

    d = {}
    for line in codecs.open(fn, 'r', 'utf-8'):
        zhwiki, baidu = line.strip('\n').rsplit('\t', 1)
        if not zhwiki in d:
            d[zhwiki] = []
        d[zhwiki].append(baidu)
    return d

if __name__=="__main__":
    enwiki_zhwiki = read_enwiki_zhwiki(ENWIKI_ZHWIKI)
    zhwiki_baidu  = read_zhwiki_baidu(ZHWIKI_BAIDU)
    find_enwiki_baidu(enwiki_zhwiki, zhwiki_baidu, ENWIKI_BAIDU)


