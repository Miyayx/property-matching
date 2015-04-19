#!/usr/bin/python
#-*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from infobox_crawler import settings
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment

import os 
import codecs
import urllib

def parse_tr(html, Type='td'):
    """
    对infobox的cell进行处理，处理th还是td通过Type决定，两者处理机制基本一样
    """
    print "Type:",Type
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
            t += child.text.strip('\n').strip()
    return t

class InfoboxSpider(scrapy.Spider):
    name = "infobox"
    allowed_domains = [""]
    start_urls = [
    ]

    def __init__(self):
        #url = "https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E5%9C%8B%E6%97%97"
        #url = "https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD"
        #url = "http://en.wikipedia.org/wiki/Albert_Einstein"
        #url = "http://zh.wikipedia.org/zh-cn/不列颠哥伦比亚"
        #self.start_urls.append(url)
        self.fo = None
        self.count = 0 #
        self.read_url()

    def read_url(self):
        fname = settings.ZHWIKI_FILE if "zhwiki" == settings.WIKI else settings.ENWIKI_FILE
        print "Infobox File:",fname
        url = settings.ZHWIKI_URL if "zhwiki" == settings.WIKI else settings.ENWIKI_URL
        output = settings.ZHWIKI_OUTPUT if "zhwiki" == settings.WIKI else settings.ENWIKI_OUTPUT
        self.fo = open(output, 'w')
        for line in open(fname):
            if "Infobox " in line:
                title = line.split('\t\t')[0]
                InfoboxSpider.start_urls.append(os.path.join(url,title))
        print "URLs:",len(InfoboxSpider.start_urls)

    def parse(self, response):
        #print urllib.urlencode(response.url)
        print urllib.unquote(response.url)
        title = urllib.unquote(response.url.split('/')[-1])
        self.count += 1
        print self.count,title
        sel = Selector(response=response)
        boxes = sel.xpath('//table[contains(@class,"infobox")]')
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
        print line
        if self.fo:
            self.fo.write(line)
            self.fo.flush()
                    #print th_t+":",td_t


