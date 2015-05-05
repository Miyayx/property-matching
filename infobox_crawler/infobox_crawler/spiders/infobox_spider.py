#!/usr/bin/python
#-*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from infobox_crawler import settings
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment

import os 
import codecs
import urllib
import urllib2

def read_finished(fn):
    return [line.split('\t\t')[0] for line in open(fn)]

def parse_tr(html, Type='td'):
    """
    对infobox的cell进行处理，处理th还是td通过Type决定，两者处理机制基本一样
    """
    #print "Type:",Type
    t = ""
    soup = BeautifulSoup(html)
    children = soup.find(Type).findChildren()
    if not len(children):
        return soup.text
    for child in children:
        if 'a' == child.name and 'sup' == child.parent.name:#不要上标
            continue
        elif 'a' == child.name and child.get('title'):#有title属性的
            text = child.text.replace('\n','').strip() # 网页中的text可能有换行，用''替换下'\n'
            if child['title'] == text:
                t += '[[%s]]'%(child['title'])
            else:
                t+='[[%s|%s]]'%(child['title'], text) #有链接的提取出来
        elif isinstance(child, NavigableString) and not isinstance(child, Comment):
            t += child.strip('\n').strip()#看看有没有纯文本
        elif not len(child.findChildren()):
            t += child.text.replace('\n','').strip()
    return t

class InfoboxSpider(scrapy.Spider):
    name = "infobox"

    def __init__(self, *args, **kwargs):
        super(InfoboxSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        #url = "https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E5%9C%8B%E6%97%97"
        #url = "https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD"
        #url = "http://en.wikipedia.org/wiki/Albert_Einstein"
        #url = "http://zh.wikipedia.org/zh-cn/不列颠哥伦比亚"
        #self.start_urls.append(url)
        self.fo = None
        self.fp = None
        self.f404 = None
        self.count = 0 #
        #self.read_url()

    def start_requests(self):
        configs = settings.WIKI_CONFIG[settings.WIKI]
        fname = configs['FILE']
        print "Infobox File:",fname
        url_prefix = configs['URL_PREFIX']
        output = configs['OUTPUT']
        fn404 = configs['fail-404']
        
        fin = []
        if os.path.isfile(output):
            fin = read_finished(output)
        self.count = len(fin)

        if settings.CONTINUE: #输出文件
            self.fo = open(output, 'a')
        else:
            self.fo = open(output, 'w')

        url_404 = []
        if os.path.isfile(fn404):
            url_404 = [line.strip('\n') for line in open(fn404)]

        self.f404 = open(fn404, 'a')
       
        fi = open(fname)

        line = fi.readline()
        while(line):
            if "::::" in line: #::::证明这里有infobox
                title = line.split('\t\t')[0]
                if not title in fin:
                    url = os.path.join(url_prefix, title)
                    if url in url_404:
                        continue
                    self.start_urls.append(url)
                    if settings.URLLIB2:
                        yield self.make_requests_from_url('http://www.baidu.com', {'title': title,'no':len(self.start_urls)-1})
                    else:
                        try:
                            yield self.make_requests_from_url(url, {'title': title,'no':len(self.start_urls)-1})
                        except:
                            pass
            line = fi.readline()
        fi.close()
        print "URLs:",len(self.start_urls)

    def make_requests_from_url(self, url, meta):
       return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

    def parse_infobox(self, title, boxes):
        prop_v = []
        for box in boxes:
            trs = box.css('tr')
            for tr in trs:
                if len(tr.css('td')) == 2:
                    th = tr.css('td')[0]
                    td = tr.css('td')[1]
                else:
                    th = tr.css('th') 
                    td = tr.css('td')
                    if not th or not td:
                        continue
                    th = th[0]
                    td = td[0]
                if th and td and td.css('::text'): #只取property和value的键值对,没有th和td的话,就跳过, td没有值也跳过
                    #th 分为有链接和纯文本两种
                    th_t = parse_tr(th.extract(), Type=th.extract()[1:3])

                    # td分为有链接(链接可能有多个)，纯文本，文本与链接混合
                    #if td.css('a'):
                    td_t = parse_tr(td.extract())

                    # 这里无所谓文本顺序，尽可能保证文字的完整性，后面用cosine和抽取出来的infobox文本对比一下，找到对应
                    #else:
                    #    td_t = td.css('::text').extract()[0]

                    prop_v.append(th_t.encode('utf-8')+"::="+td_t.encode('utf-8'))
        "::;".join(prop_v)
        line = "%s\t\t%s\n"%(title, "::;".join(prop_v))
        #print line
        if self.fo:
            self.fo.write(line)
            self.fo.flush()
                    #print th_t+":",td_t

    def fetch_infobox_html(self, title, boxes):
        htmls = [b.extract().replace('\n','') for b in boxes]
        line = "%s\t\t%s\n"%(title, "::;".join(htmls).encode('utf-8'))
        #print line
        if self.fo:
            self.fo.write(line)
            self.fo.flush()

    def parse(self, response):
            
        no = response.meta['no']
        if response.status == 404:
            self.f404.write(self.start_urls[no]+'\n')

        title = response.meta['title']

        if settings.URLLIB2:
            #伪装为浏览器  
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
            headers = {'User-Agent':user_agent} 
            req = urllib2.Request(self.start_urls[no], headers=headers)  
            response = urllib2.urlopen(req)
            sel = Selector(text = response.read())
        else:
            sel = Selector(response = response)

        print urllib.unquote(response.url)

        self.count += 1
        print self.count,title
        boxes = sel.xpath('//table[contains(@class,"infobox")]')
        if settings.HTML:
            self.fetch_infobox_html(title, boxes)
        else:
            self.parse_infobox(title, boxes)


