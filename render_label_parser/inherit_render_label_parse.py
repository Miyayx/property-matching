# -*- coding:utf-8 -*-

import os
import codecs 
from fileio import *
from render_label_parse import *

from hanziconv import HanziConv

DIR = "/data/xlore20160223/Template"

#INHERIT_TEMPLATE  = os.path.join(DIR, "enwiki-template-inherit.dat")
#REDIRECT_TEMPLATE = os.path.join(DIR, "enwiki-template-redirect.dat")
#TEMPLATE_TRIPLE   = os.path.join(DIR, "enwiki-20160305-template-triple.dat")
#INHERIT_TEMPLATE_TRIPLE = os.path.join(DIR, "enwiki-20160305-inherit-template-triple.dat")
#INHERIT_TEMPLATE_DUMP = os.path.join(DIR,"enwiki-template-inherit-dump.dat")

INHERIT_TEMPLATE  = os.path.join(DIR, "zhwiki-template-inherit.dat")
REDIRECT_TEMPLATE = os.path.join(DIR, "zhwiki-template-redirect.dat")
TEMPLATE_TRIPLE   = os.path.join(DIR, "zhwiki-20160203-template-triple.dat")
INHERIT_TEMPLATE_TRIPLE = os.path.join(DIR, "zhwiki-20160203-inherit-template-triple.dat")
INHERIT_TEMPLATE_DUMP = os.path.join(DIR,"zhwiki-template-inherit-dump.dat")


def inherit_render_label_parse(label):
    THREE = r'{{{(.+)}}}'
    labels = []
    while re.search(THREE, label):
        label = re.findall(THREE, label)[0]
        l = re.split(THREE, label)[0].strip().strip('|').strip()
        l = clear_label(l)
        labels.append(l)
    return labels

def parse_inherit_doc(doc, tl_rl):
    result = {}

    if not doc:
        return result

    lines = doc.split('\n')
    i = 0 
    rl = tl = None
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and '=' in line:
            tl, rl = line.strip('|').strip().split('=',1)
            tl = tl.strip()
            rl = rl.strip()
            #print tl, rl
            #print tl_rl
            if re.search(THREE_REGEX, rl):
                rls = inherit_render_label_parse(rl)
                for r in rls:
                    print 'Render label:', r
                for RL in (rls + [render_label_parse(rl)]):
                    if RL in tl_rl:
                        result[tl] = tl_rl[RL]
                        break
                if not tl in result and rls:
                    result[tl] = rls[-1]

            elif len(rl) > 0:
                #| timezone1               = [[歐洲中部時間|CET]]
                result[tl] = rl
            else: #len(rl) == 0
                if tl in tl_rl:
                    result[tl] = tl_rl[tl]

        i += 1
    return result

def parse_inherit(doc, lower_redirect_tems, redirect_tems, tem_triple):
    utf8_parser = ET.XMLParser(encoding='utf-8')
    try:
        doc = doc.encode('utf-8')
    except:
        pass
    tree = ET.parse(StringIO(doc), parser=utf8_parser)
    root = tree.getroot()
    title = root.find(".//title").text.strip()
    revision = root.find(".//revision")
    text = revision.find(".//text").text
    if text != None:
        firstline = text.lower().split('\n')[0].strip('\n').strip()
        secondline = None
        if len(text.split('\n')) > 1:
            secondline = text.lower().split('\n')[1].strip('\n').strip()
        parent_tem = None
        if re.search(r'{{\s*infobox.+', firstline) or re.search(ur'{{\s*艺人', firstline):
            #print 'firstline', firstline
            parent_tem = re.findall(r'{{(.+?)$', firstline)[0]
        elif secondline and re.search(r'{{\s*infobox.+', secondline.lower()):
            #print 'secondline', secondline
            parent_tem = re.findall(r'{{(.+?)$', secondline)[0]
        parent_tem = parent_tem.replace('infobox', 'Infobox').replace('_',' ')
        parent_tem = 'Template:'+parent_tem
        parent_tem = HanziConv.toSimplified(parent_tem)

        if parent_tem.lower() in lower_redirect_tems:
            parent_tem = lower_redirect_tems[parent_tem.lower()]
        if parent_tem in redirect_tems:
            #print parent_tem, "in redirect_tems"
            parent_tem = redirect_tems[parent_tem]
        #print parent_tem
        if parent_tem in tem_triple:
            #print parent_tem, "in tem_triple"
            result = parse_inherit_doc(text, tem_triple[parent_tem])
            return result, parent_tem

    return {},  None


def main():
    fw = codecs.open(INHERIT_TEMPLATE_TRIPLE, 'w', 'utf-8')
    parsed_count = new_properties = 0

    #政府信息框，气候数据
    zhengfu = qihou = 0

    inherit_tems = read_inherit_template(INHERIT_TEMPLATE)
    redirect_tems = read_redirect_template(REDIRECT_TEMPLATE)
    tem_triple    = read_template_triple(TEMPLATE_TRIPLE)

    left_tems = []

    lower_redirect_tems = {}
    for k in redirect_tems:
        lower_redirect_tems[k.lower()] = k
    for k in tem_triple:
        lower_redirect_tems[k.lower()] = k

    for title, doc in read_template_dump(INHERIT_TEMPLATE_DUMP):
        if title in inherit_tems:
            result, parent_tem = parse_inherit(doc, lower_redirect_tems, redirect_tems, tem_triple)
            new_properties += len(result)
            if len(result) and parent_tem:
                parsed_count += 1
            elif u'政府信息框' in title:
                zhengfu += 1
            elif u'气候数据' in title:
                qihou += 1
            else:
                left_tems.append(title)

            for tl, rl in result.iteritems():
                title = HanziConv.toSimplified(title)
                tl = HanziConv.toSimplified(tl)
                rl = HanziConv.toSimplified(rl)
                parent_tem = HanziConv.toSimplified(parent_tem)
                fw.write(title+'\t'+tl+'\t'+rl+'\t'+parent_tem+'\n')
            fw.flush()

    fw.close()

    print "Total Inherit Templates:",len(inherit_tems)
    print "Parsed Inherit Templates:", parsed_count
    print "政府信息框:", zhengfu
    print "气候数据:",qihou
    print "New Properties:", new_properties
    print "Left:",len(left_tems)

    WIKI = INHERIT_TEMPLATE.split('/')[-1].split('-')[0]

    with codecs.open(WIKI+'-left-inherit-template.dat', 'w', 'utf-8') as f:
        for t in sorted(left_tems):
            f.write(t+'\n')


if __name__=="__main__":
    import time
    start = time.time()

    main()

    print 'Time Consuming:',time.time()-start

