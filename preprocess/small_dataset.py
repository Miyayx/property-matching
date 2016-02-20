#-*- coding:utf-8 -*-

import os
import codecs

TEMPLATES=("template:infobox film", "template:infobox actor", "template:infobox company", "template:infobox galaxy")

BAIDU_DIR = "/home/xlore/server36/baikedump/"
BAIDU_INFOBOX=os.path.join(BAIDU_DIR, "baidu-title-property.dat")
BAIDU_INSTANCE_CONCEPT=os.path.join(BAIDU_DIR, "baidu-instance-concept.dat")

ENWIKI_DIR = "/home/xlore/disk2/raw.wiki/"
ENWIKI_INFOBOX=os.path.join(ENWIKI_DIR, "enwiki-infobox-new.dat")
ENWIKI_INSTANCE_CONCEPT=os.path.join(ENWIKI_DIR, "enwiki-category.dat")

SMALL_DIR="/home/xlore/server36/infobox/small"
SMALL_BAIDU_INFOBOX=os.path.join(SMALL_DIR, "small-baidu-title-property.dat")
SMALL_BAIDU_INSTANCE_CONCEPT=os.path.join(SMALL_DIR, "small-baidu-instance-concept.dat")
SMALL_ENWIKI_INFOBOX=os.path.join(SMALL_DIR, "small-enwiki-infobox.dat")
SMALL_ENWIKI_INSTANCE_CONCEPT=os.path.join(SMALL_DIR, "small-enwiki-category.dat")

wiki_articles = set()
fw1 = codecs.open(SMALL_ENWIKI_INFOBOX, 'w', 'utf-8')
for line in codecs.open(ENWIKI_INFOBOX, 'r', 'utf-8'):
    if not '\t\t' in line:
        continue
    title, info = line.strip('\n').split('\t\t')
    info = info.split('\t')[0]
    tem, infobox = info.split(':::::',1)
    tem = 'template:'+tem
    if tem in TEMPLATES:
        wiki_articles.add(title)
        fw1.write(line)
        fw1.flush()
fw1.close()

fw2 = codecs.open(SMALL_ENWIKI_INSTANCE_CONCEPT, 'w', 'utf-8')
for line in codecs.open(ENWIKI_INSTANCE_CONCEPT, 'r', 'utf-8'):
    a, c = line.split('\t\t')
    if a in wiki_articles:
        fw2.write(line)
        fw2.flush()
fw2.close()

baidu_articles = set()
count = 0
fw3 = codecs.open(SMALL_BAIDU_INFOBOX, 'w', 'utf-8')
for line in codecs.open(BAIDU_INFOBOX, 'r', 'utf-8'):
    if count > 500000:
        break
    else:
        baidu_articles.add(line.split('\t')[0])
        fw3.write(line)
        fw3.flush()
fw3.close()
        
fw4 = codecs.open(SMALL_BAIDU_INSTANCE_CONCEPT, 'w', 'utf-8')
for line in codecs.open(BAIDU_INSTANCE_CONCEPT, 'r', 'utf-8'):
    try:
        a, c = line.split('\t')
        if a in baidu_articles:
            fw4.write(line)
            fw4.flush()
    except:
        print 'Read Error:',line
fw4.close()

