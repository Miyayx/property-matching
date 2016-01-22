#-*- coding:utf-8 -*-

import urllib
import json
import sys,os  
import codecs

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

class Translater:
    BAIDU_API_KEY="n2dfnNcQZobspd8SYUGvyvsy"
    API_URL=("http://openapi.baidu.com/public/2.0/bmt/translate?client_id=" + BAIDU_API_KEY + "&q=%s&from=%s&to=%s")

    def __init__(self):
        pass

    def translate(self, s, source_lan="en", target_lan="zh"):
        URL = "http://openapi.baidu.com/public/2.0/bmt/translate?client_id=%s&from=%s&to=%s&q="%(Translater.BAIDU_API_KEY, source_lan, target_lan)
        j = urllib.urlopen((URL+s).encode("UTF-8")).read()
        #print j
        return self.parse_json(j)

    def parse_json(self, j):
        d = {}
        Json = json.loads(j)
        if not 'trans_result' in Json:
            return d
        for item in Json['trans_result']:
            src, dst = item['src'], item['dst']
            d[src] = dst
        return d

def start(fi, fo):
    translater = Translater()
    fw = codecs.open(fo, 'w', 'utf-8')
    for line in codecs.open(fi, 'r', 'utf-8'):
        if len(line.split('\t\t')) < 2:
            fw.write(line)
        else:
            article, infos = line.strip('\n').split('\t\t')
            new_infos = []
            for info in infos.split('\t'):
                tem, facts = info.split(':::::', 1)
                queries = []
                for fact in facts.split('::::;'):
                    if len(fact.split('::::=')) < 2:
                        continue
                    k, v = fact.split('::::=')
                    if is_number(v):
                        continue
                    if '[[' in v:
                        v = v.replace('[[','').replace(']]','').split('|')[0]
                    queries.append(v)
                res = translater.translate('\n'.join(queries))
                for k, v in res.iteritems():
                    #print 'replace',k,'to',v
                    info = info.replace(k ,v)
                    #print 'new line:',info
                new_infos.append(tem+':::::'+info)
                print info
            fw.write('%s\t\t%s\n'%(article, '\t'.join(new_infos)))
            fw.flush()
    fw.close()

def translate_test():
    s = 'This is a test'
    print Translater().translate(s)

if __name__=="__main__":
    if len(sys.argv) < 3:  
       print 'No input and output files'  
       sys.exit()  

    fi, fo = sys.argv[1], sys.argv[2]
    start(fi, fo)

    #translate_test()

  
