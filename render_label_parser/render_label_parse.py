# -*- coding:utf-8 -*-

import json
import re,os
import codecs
import urllib2
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen
    from urllib import urlencode

#import mwparserfromhell
import socks
import socket

from StringIO import StringIO

import xml.etree.ElementTree as ET

from hanziconv import HanziConv
import mwparserfromhell

"""
通过给的template list， 从网页中爬取， 或从dump文件中抽取显示label

"""
import sys
sys.path.append('..')
from utils.logger import *
initialize_logger('./render_label.log')

class TemplateType:
    OTHER = 0
    INFOBOX = 1
    EXTENSION = 2
    TABLE = 3
    REDIRECT = 4

API_URL = "https://zh.wikipedia.org/w/api.php"

INPUT = "zhwiki-template-name.dat"
#OUTPUT = "enwiki-template-triple-new.dat"
OUTPUT = "zhwiki-template-triple-new.dat"

IF_REGEX = r"{{#if:.+}}"
THREE_REGEX = r"{{{.+?}}}"
THREE_CONTAIN_REGEX = r"{{{(.+?)}}}"
THREE_QUOTATION = r"'''(.+?)'''"
LONGITEM_REGEX = r"{{longitem.+}}"
NOWRAP_REGEX = r'{{nowrap\|(.+)}}'
SPAN_REGEX = r'\<span.+?\>(.+)\</span\>'
COMMENT_REGEX = r'\<!--.+-\>'
LINK_REGEX = r'\[\[.+\]\]'
REDIRECT_REGEX = ur'#(?:REDIRECT|重定向).*\[\[(.+?)\]\]'
#TH_REGEX = r'\<th.*?\>(.+?)\</th\>'
TH_REGEX = r'\<th.*?\>(.+?)\</'
TD_REGEX = r'\<td.*?\>(.+?)\</td\>'
TD_THREE_REGEX = r'\<td.*?\>{{{(.+?)}}}\</td\>'

def convert_to_simplified(text):
    if u'歷' in text:
        text = text.replace(u'歷', u'历')
    return HanziConv.toSimplified(text)

def if_parse(s):
    stack = []
    result = {}

    #print 'IF parse', s,'...'
    i = 0
    while i < len(s):
        if s[i:].startswith('{{#if:'):
            stack.append(('{{#if:', i+6))
            i += (6)
        elif s[i:].startswith('|{{#if:'):
            stack.append(('|{{#if:', i+7))
            i += (7)
        elif s[i:].startswith('{{{'):
            stack.append(('{{{', i+3))
            i += (3)
        elif s[i:].startswith('|}}}|'):
            t = stack.pop()
            j = t[1] #上一个{{{的下标   
            condition = s[j:i] #if条件中的template label 
            i += 5
            k = 0
            if '{' in s[i:]:
                k = i + s[i:].index('}')
            elif '|' in s[i:]:
                k = i + s[i:].index('|')
            else:
                k = i + s[i:].index('}')
            suffix = s[i:k].split('|')[0] #目前就选第一个
            if not '{' in suffix:
                result[condition] = suffix  #有抽错的情况
                #print condition, suffix
            if '{' in s[i:]:
                i = i + s[i:].index('{')
            else:
                i = i + s[i:].index('}')

        elif s[i:].startswith('}}'):
            if len(stack) > 0:
                stack.pop()
            else:
                print "Stack Wrong..."
            i += 2
        else:
            #print s[i:]
            i += 1
    return result

def render_label_parse(label):
    """
    Examples:
    Story by
    <span class"nowrap">Spouse(s)</span>
    {{longitem |Production<br/>compan{{#if:{{{production companies|}}}|ies|y}} }}
    {{longitem|stylewhite-space:normal; |Release dates}}
    {{#if:{{{burial_place|}}}|Burial place|Resting place}}
    Parent{{#if:{{{parents|}}}|(s)|{{#if:{{{father|}}}|{{#if:{{{mother|}}}|s|(s)}}|(s)}}}}
    Predecessor{{#if:{{{predecessors|}}}|s}}

    """
    #print 'Parsing', label, '...'
    if re.match(LONGITEM_REGEX, label): #从头匹配
        label = label.strip('{{').strip('}}').strip().split('|', 1)[1] #删除longitem部分
    if re.search(IF_REGEX, label):
        IFs = re.findall(IF_REGEX, label)
        for IF in IFs:
            suffixes = if_parse(IF)
            if len(suffixes) > 0:
                suffix = suffixes.values()[0] #这也只能选一个
            else:
                suffix = ''
            label = label.replace(IF, suffix)

    if re.search(LINK_REGEX, label):
        pass
    else:
        label = label.split('|')[-1]
    label = label.replace('<br/>', ' ')
    label = label.replace('&nbsp;', ' ')
    if re.search(NOWRAP_REGEX, label):
        label = re.findall(NOWRAP_REGEX, label)[0]
    if re.search(SPAN_REGEX, label):
        label = re.findall(SPAN_REGEX, label)[0]
    if re.search(COMMENT_REGEX, label):
        comment= re.findall(COMMENT_REGEX, label)[0]
        label = label.replace(comment, '')
    return label

#print render_label_parse('<span style="white-space:nowrap;">Notable credit(s)</span>')
#print render_label_parse('{{longitem |Production<br/>compan{{#if:{{{production companies|}}}|ies|y}} }}')
#print render_label_parse('{{longitem|stylewhite-space:normal; |Release dates}}')
#print render_label_parse('{{#if:{{{burial_place|}}}|Burial place|Resting place}}')
#print render_label_parse('Parent{{#if:{{{parents|}}}|(s)|{{#if:{{{father|}}}|{{#if:{{{mother|}}}|s|(s)}}|(s)}}}}')
#print render_label_parse('Predecessor{{#if:{{{predecessors|}}}|s}}')

def template_label_parse(label):
    """
    Return: list of template labels

    Examples:
    {{{based_on|{{{based on|}}}}}}
    {{#if:{{{production companies|{{{studio|}}}}}} |<div style"vertical-align:middle;">{{{production companies|{{{studio|}}}}}}</div>}}
    {{{weapon<includeonly>|</includeonly>}}}
    """
    label = label.replace('<includeonly>','').replace('</includeonly>','')
    label = clear_label(label)
    labels = set()
    if re.search(THREE_REGEX, label):
        threes = re.findall(THREE_REGEX, label)
        for three in threes:
            items = three.replace('{{{','').replace('}}}','').split('|')
            for i in items:
                i = i.strip()
                if len(i) == 0:
                    continue
                #if '{' in i or '}' in i:  #抽错了，先舍弃掉
                #    continue
                labels.add(i)
    return labels

def clear_label(label):
    label = label.replace('</noinclude>', '').replace('<noinclude>', '')
    label = label.replace('<includeonly>', '').replace('</includeonly>','')
    nowrap = re.search(r'{{nowrap|.+?}}', label)
    if nowrap:
        label = label.replace(re.findall(r'{{nowrap|.+?}}', label)[0], re.findall(r'{{nowrap|(.+?)}}', label)[0])
    return label

#print template_label_parse("{{#if:{{{production companies|{{{studio|}}}}}} |<div style'vertical-align:middle;'>{{{production companies|{{{studio|}}}}}}</div>}}")

def clawer(template):

    print 'Clawer', template, '...'
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
            }
    req_timeout = 5

    data = {"action": "query", "prop": "revisions", "rvlimit": 1,
            "rvprop": "content", "format": "json", "titles": template}
    #raw = urlopen(API_URL, urlencode(data).encode()).read()
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1085)
    socket.socket = socks.socksocket

    #proxy = urllib2.ProxyHandler({'http': '127.0.0.1:1085'})
    #opener = urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)

    req = urllib2.Request(API_URL, urlencode(data).encode(),req_header)
    raw = urllib2.urlopen(req).read()
    res = json.loads(raw)
    if not "revisions" in res["query"]["pages"].values()[0]:
        print "No info for", template
        return

    text = res["query"]["pages"].values()[0]["revisions"][0]["*"]
    if text.startswith("#REDIRECT"):
        if re.search(LINK_REGEX, text):
            text = re.findall(LINK_REGEX, text)[0].strip('[[').strip(']]').strip()
            print template, "redirect to", text
            return clawer(text)
    return mwparserfromhell.parse(text)

def parse_by_api(template):
    doc = clawer(template)
    return parse_doc(template, doc)

def template_type(doc):
    utf8_parser = ET.XMLParser(encoding='utf-8')
    #print doc
    try:
        doc = doc.encode('utf-8')
    except:
        pass
    tree = ET.parse(StringIO(doc), parser=utf8_parser)
    root = tree.getroot()
    title = root.find(".//title").text.strip()
    redirect = root.find(".//redirect")
    if not redirect == None:
        return TemplateType.REDIRECT
    revision = root.find(".//revision")
    text = revision.find(".//text").text

    if text != None:
        firstline = text.lower().split('\n')[0].strip('\n').strip().replace(' ','')

        secondline = None
        if len(text.split('\n')) > 1:
            secondline = text.lower().split('\n')[1].strip('\n').strip().replace(' ','')

        if firstline.endswith('{{infobox') or firstline.endswith(u'{{艺人') or '{{infobox\n'in text or (secondline and secondline.endswith('{{infobox')):
            #print text.lower().split('\n')[0]
            return TemplateType.INFOBOX
        elif '{{infobox' in firstline or (secondline and '{{infobox' in secondline):
            #print text.lower().split('\n')[0]
            return TemplateType.EXTENSION
        elif 'class="infobox' in firstline or (secondline and 'class="infobox' in secondline):
            return TemplateType.TABLE
        #elif re.search(REDIRECT_REGEX, text.strip()):
        #    return TemplateType.REDIRECT
        else:
            return TemplateType.OTHER
    else:
        return TemplateType.OTHER

def parse_redirect(title, doc):
    redirect = re.findall(REDIRECT_REGEX, doc)[0]
    redirect = redirect.replace('template','Template').replace('_',' ')
    return {title : redirect}

def parse_by_dump(doc):
    utf8_parser = ET.XMLParser(encoding='utf-8')
    #print doc
    try:
        doc = doc.encode('utf-8')
    except:
        pass
    tree = ET.parse(StringIO(doc), parser=utf8_parser)
    root = tree.getroot()
    title = root.find(".//title").text.strip()
    redirect = root.find(".//redirect")
    revision = root.find(".//revision")
    text = revision.find(".//text").text
    ttype = template_type(doc)
    if ttype == TemplateType.INFOBOX or ttype == TemplateType.EXTENSION:
        return ttype, parse_doc(title, text)
    elif ttype == TemplateType.TABLE: 
        return ttype, parse_table(title, text)
    elif ttype == TemplateType.REDIRECT:
        return ttype, {title: redirect.get('title')}
    else:
        return ttype, {}

def parse_table(template, doc):
    """
    https://zh.wikipedia.org/w/index.php?title=Template:Infobox_%E8%88%AA%E7%A9%BA%E5%99%A8&action=edit
    https://zh.wikipedia.org/w/index.php?title=Template:%E5%93%88%E5%88%A9%C2%B7%E6%B3%A2%E7%89%B9%E4%BA%BA%E7%89%A9&action=edit
    https://zh.wikipedia.org/w/index.php?title=Template:Infobox_lake&action=edit
    """
    result = {}

    if not doc:
        return result

    wikicode = mwparserfromhell.parse(doc)
    templates = wikicode.filter_templates()
    for line in templates:
        line = line.replace('\n','')
        #print line
        if line.startswith('{{#if:') and re.search(THREE_QUOTATION, line):
            #  #if:{{{designer|}}}|<tr><td style="text-align:right;">'''設計者'''</td><td>{{{designer}}}</td></tr>
            tls = re.findall(THREE_CONTAIN_REGEX, line)
            if not tls:
                print "not:", line
                continue
            tl = tls[0]
            tl = clear_label(tl).strip('|')
            rl = re.findall(THREE_QUOTATION, line)[0]
            result[template+'\t'+tl] = rl
            print tl, rl
        elif (line.startswith('{{#if:') or line.startswith('{{#ifeq:')) and '<th' in line:
            tls = re.findall(THREE_CONTAIN_REGEX, line)
            if not tls:
                print "not:", line
                continue
            tl = tls[0]
            tl = clear_label(tl).strip('|')
            rl = re.findall(TH_REGEX, line)[0].strip().strip(u'：').strip(u':')
            result[template+'\t'+tl] = rl
            print tl, rl
        elif (line.startswith('{{#if:') or line.startswith('{{#ifeq:')) and '<td' in line:
            tls = re.findall(THREE_CONTAIN_REGEX, line)
            if not tls:
                print "not:", line
                continue
            tl = tls[0]
            tl = clear_label(tl).strip('|')
            rls = re.findall(TD_THREE_REGEX, line)
            if rls:
                rl = rls[0]
                result[template+'\t'+tl] = rl
                print tl, rl
            else:
                rls = re.findall(TD_REGEX, line)
                if rls:
                    rl = rls[0]
                    result[template+'\t'+tl] = rl
                    print tl, rl
        elif (line.startswith('{{#if:') or line.startswith('{{#ifeq:')) and '! ' in line:
            tls = re.findall(THREE_CONTAIN_REGEX, line)
            if not tls:
                print "not:", line
                continue
            tl = tls[0]
            tl = clear_label(tl).split('|')[0]
            print line
            rls = re.findall(r'!\s(.+?){{!}}', line)
            if rls:
                rl = rls[0].strip()
                result[template+'\t'+tl] = rl
                print tl, rl

    if len(result) == 0:
        lines = doc.split('\n')
        i = 0 
        rl = tl = None
        while i < len(lines):
            line = lines[i].strip()
            if re.search(THREE_QUOTATION, line) and re.search(THREE_REGEX, line):
                TL = re.findall(THREE_CONTAIN_REGEX, line)[0]
                TL = clear_label(TL).strip('|')
                RL = re.findall(THREE_QUOTATION, line)[0]
                result[template+'\t'+TL] = RL
                print TL, RL
            i += 1

    return result

def parse_doc(template, doc):
    result = {}

    if not doc:
        return result

    lines = doc.split('\n')
    i = 0 
    rl = tl = None
    n = "0"
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|'):
            line = line.strip().strip('|').strip()
            print line
            if (line.startswith('label') or line.startswith('header')) and '=' in line:
                label, rl = line.split('=', 1)
                if not re.search(r'\d+', label):
                    i += 1
                    continue
                label = label.strip('\t').strip()
                rl = rl.strip('\t').strip()
                n = re.findall(r'\d+', label)[0]

            if line.startswith('data') and '=' in line:
                label, tl = line.split('=', 1)
                if not re.search(r'\d+', label): #没有data后没有数字，不解析
                    i += 1
                    continue
                label = label.strip('\t').strip()
                tl = tl.strip('\t').strip()
                m = re.findall(r'\d+', label)[0]
                if n == m:
                    #print '&'*10
                    #print tl
                    #print rl
                    RL = render_label_parse(rl)
                    TLS = template_label_parse(tl)
                    for TL in TLS:
                        #print template + '\t' + TL + '\t' + RL
                        result[template+'\t'+TL] = RL
                else:
                    n = "0"
                    rl = tl = None
        i += 1
    return result

def read_templates(fn, fo):
    tems = []
    have = set()

    from shutil import copyfile
    import time
    if os.path.isfile(fo):
        copyfile(fo, fo+'-'+str(time.strftime("%Y-%m-%d %H:%M")))

        for line in codecs.open(fo, 'r' 'utf-8'):
            have.add(line.strip('\n').split('\t')[0])
        print 'Have parsed',len(have),'templates'

    for line in codecs.open(fn, 'r' 'utf-8'):
        t = None
        if line.lower().startswith('template'):
            t = line.strip('\n')
        else:
            t = 'Template:'+line.strip('\n')
        if t in have:
            continue
        tems.append(t)
    return tems

def read_template_dump(fn):
    s = ""
    fr = codecs.open(fn, 'r', 'utf-8')
    line = fr.readline()
    while line:
        if line.startswith('<page>'):
            s += line
            line = fr.readline()
            title = line.strip().replace('<title>','').replace('</title>','')
            while not '</page>' in line:
                s += line
                line = fr.readline()
            s += line
            yield title, s

            s = ""
        line = fr.readline()

def dump_parse(fn, fo, redirect_fn):
    Tn = not_infobox_Tn = not_have_p_Tn = 0
    extensions = set()
    tables = set()
    infoboxes = set()
    redirect = dict()
    fw = codecs.open(fo, 'w', 'utf-8')
    fw2 = codecs.open('no_property_infobox_template', 'w', 'utf-8')
    fw_infobox = codecs.open('no_property_infobox_template_infobox', 'w', 'utf-8')
    fw_table = codecs.open('no_property_infobox_template_table', 'w', 'utf-8')
    for title, doc in read_template_dump(fn):
        Tn += 1
        ttype, result = parse_by_dump(doc)
        if ttype == TemplateType.OTHER:
            not_infobox_Tn += 1
            continue
        elif ttype == TemplateType.REDIRECT:
            not_infobox_Tn += 1
            redirect.update(result)
            continue
        elif len(result) == 0:
            #fw.write(title+'\n')
            if ttype == TemplateType.INFOBOX:
                fw_infobox.write(title+'\n')
            elif ttype == TemplateType.TABLE:
                fw_table.write(title+'\n')
            else:
                fw2.write(title+'\n')
            
            not_have_p_Tn += 1
        else:
            for k, v in sorted(result.iteritems()):
                #k = convert_to_simplified(k)
                v = convert_to_simplified(v)
                fw.write(k+'\t'+v+'\n')
        fw.flush()

        if ttype == TemplateType.EXTENSION:
            extensions.add(title)
            #extension += 1
        elif ttype == TemplateType.TABLE:
            tables.add(title)
            #table += 1
        elif ttype == TemplateType.INFOBOX:
            infoboxes.add(title)
            #infobox += 1

    logging.info("Template Total: %d"%Tn)
    logging.info("Infobox Template: %d"%(Tn - not_infobox_Tn))
    logging.info("Have Property Infobox Template: %d"%(Tn - not_infobox_Tn - not_have_p_Tn))
    logging.info("Infobox: %d"%len(infoboxes))
    logging.info("Extension: %d"%len(extensions))
    logging.info("Table:%d"%len(tables))
    logging.info("Redirect:%d"%len(redirect))

    fw.close()
    fw2.close()
    fw_infobox.close()
    fw_table.close()

    re_fw = codecs.open(redirect_fn, 'w', 'utf-8') 
    for k, v in redirect.iteritems():
        if v in extensions or v in tables or v in infoboxes:
            #只记录infobox template的redirect信息
            try:
                re_fw.write(convert_to_simplified(k)+'\t'+convert_to_simplified(v)+'\n')
            except:
                print k,v
                pass
    re_fw.close()

#parse('Template:infobox film')
#parse('Template:infobox person')
#parse('Template:infobox com')
#parse_by_api('Template:Infobox 最終幻想角色')

#if __name__ == "__main__":
#
#    templates = read_templates(INPUT, OUTPUT)
#    fw = codecs.open(OUTPUT, 'a', 'utf-8')
#    for t in templates:
#        result = parse(t)
#         if result == None:  #不是infobox template
#             pass
#        if len(result) == 0:
#            fw.write(t+'\n')
#        else:
#            for k, v in sorted(result.iteritems()):
#                fw.write(k+'\t'+v+'\n')
#        fw.flush()
#
#    fw.close()

if __name__ == "__main__":
    """
    1. template dump
    2. template-triple
    3. template-redirect
    """
    import sys
    import time
    start = time.time()
    if len(sys.argv) < 2:
        print "not input and output filename"
        exit()

    dump_parse(sys.argv[1], sys.argv[2], sys.argv[3])
    print 'Time Consuming:',time.time()-start

