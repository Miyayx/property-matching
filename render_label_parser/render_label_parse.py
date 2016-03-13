# -*- coding:utf-8 -*-

import json
import re,os
import codecs
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen
    from urllib import urlencode

import mwparserfromhell

API_URL = "https://en.wikipedia.org/w/api.php"

INPUT = "enwiki-template-name.dat"
OUTPUT = "enwiki-template-triple-new.dat"
#OUTPUT = "zhwiki-template-triple-new.dat"

IF_REGEX = r"{{#if:.+}}"
THREE_REGEX = r"{{{.+?\|}}}"
LONGITEM_REGEX = r"{{longitem.+}}"
NOWRAP_REGEX = r'{{nowrap\|(.+)}}'
SPAN_REGEX = r'\<span.+?\>(.+)\</span\>'
COMMENT_REGEX = r'\<!--.+-\>'
LINK_REGEX = r'\[\[.+\]\]'

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
    """
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

#print template_label_parse("{{#if:{{{production companies|{{{studio|}}}}}} |<div style'vertical-align:middle;'>{{{production companies|{{{studio|}}}}}}</div>}}")

def clawer(template):
    data = {"action": "query", "prop": "revisions", "rvlimit": 1,
            "rvprop": "content", "format": "json", "titles": template}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw)
    if not "revisions" in res["query"]["pages"].values()[0]:
        print "No info for", template
        return
    
    text = res["query"]["pages"].values()[0]["revisions"][0]["*"]
    if text.startswith("#REDIRECT"):
        if re.search(LINK_REGEX, text):
            text = re.findall(LINK_REGEX, text).strip('[[').split(']]').strip()
            print template, "redirect to", text
            return clawer(text)
    return mwparserfromhell.parse(text)

def parse(template):
    result = {}

    doc = clawer(template)
    if not doc:
        return result

    lines = doc.split('\n')
    i = 0 
    rl = tl = None
    n = "0"
    while i < len(lines):
        line = lines[i]
        if line.startswith('|'):
            line = line.strip().strip('|').strip()

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
                    print '&'*10
                    #print tl
                    #print rl
                    RL = render_label_parse(rl)
                    TLS = template_label_parse(tl)
                    for TL in TLS:
                        print template + '\t' + TL + '\t' + RL
                        result[template+'\t'+TL] = RL
                else:
                    n = 0
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

#parse('Template:infobox film')
#parse('Template:infobox person')
#parse('Template:infobox com')

if __name__ == "__main__":

    templates = read_templates(INPUT, OUTPUT)
    fw = codecs.open(OUTPUT, 'a', 'utf-8')
    for t in templates:
        results = parse(t)
        if len(results) == 0:
            fw.write(t+'\n')
        else:
            for k, v in sorted(results.iteritems()):
                fw.write(k+'\t'+v+'\n')
        fw.flush()

    fw.close()

