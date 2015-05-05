#-*- coding:utf-8 -*-

import scrapy
from scrapy.http import Request

from template_crawler import settings
from bs4 import BeautifulSoup

import os
import codecs
import urllib
import urllib2

def read_finished(fn):
    return [line.split('\t\t')[0] for line in open(fn)]

class LabelSpider(scrapy.spider.Spider):
    name = "label"


    def __init__(self, *args, **kwargs):
        super(LabelSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        #url = "http://zh.wikipedia.org/wiki/Template:ONE_PIECE%E4%BA%BA%E7%89%A9"
        #self.start_urls.append(url)
        self.fo = None
        self.htmlfo = None
        self.f404 = None
        self.count = 0 #
        #self.read_url()

    def start_requests(self):
        configs = settings.WIKI_CONFIG[settings.WIKI]
        fname = configs['FILE']
        print "Infobox File:",fname
        url_prefix = configs['URL_PREFIX']
        output = configs['OUTPUT']
        html_output = configs['HTML_OUTPUT']
        fn404 = configs['fail-404']
        
        fin = []
        if os.path.isfile(output):
            fin = read_finished(output)
        self.count = len(fin)

        if settings.CONTINUE: #输出文件
            self.fo = open(output, 'a')
            self.htmlfo = open(html_output, 'a')
        else:
            self.fo = open(output, 'w')
            self.htmlfo = open(html_output, 'w')

        url_404 = []
        if os.path.isfile(fn404):
            url_404 = [line.strip('\n') for line in open(fn404)]

        self.f404 = open(fn404, 'a')
       
        fi = open(fname)

        line = fi.readline()
        while(line):
            title = line.strip('\n')
            if not 'Infobox' in title: #只分析infobox
                line = fi.readline()
                continue
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
                        #yield self.make_requests_from_url('http://zh.wikipedia.org/wiki/Template:Infobox_Peri_GR', {'title': title,'no':len(self.start_urls)-1})
                        #break
                    except:
                        pass
            line = fi.readline()
        fi.close()
        print "URLs:",len(self.start_urls)

    def make_requests_from_url(self, url, meta):
       return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

    def parse_infobox(self, title, box):
        trs = []
        for tr in box.findAll('tr'):
            children = tr.find_all(True, recursive=False)
            if len(children) == 2:
                th, td = children
                label = ""
                if th.find('a'):#有链接处理链接
                    a = th.find('a')
                    if a['title'] == th.text.strip():
                        label = '[[[%s]]]'%a['title']
                    else:
                        label = '[[[%s|%s]]]'%(a['title'], th.text)
                else:
                    label = th.text.strip()
                trs.append(label+':::'+td.text.strip())
        labels = "::;".join(trs)
        try:
            labels = labels.encode('utf-8')
        except:
            pass
        try:
            title = title.encode('utf-8')
        except:
            pass

        line = "%s\t\t%s\n"%(title, labels.replace('\n',' '))
        print line
        if self.fo:
            self.fo.write(line)
            self.fo.flush()

    def fetch_infobox_html(self, title, box):
        """
        爬取infobox的html并保留
        """
        line = "%s\t\t%s\n"%(title, str(box).replace('\n',''))
        #print line
        if self.htmlfo:
            self.htmlfo.write(line)
            self.htmlfo.flush()

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
            soup = BeautifulSoup(response.read())
        else:
            soup = BeautifulSoup(response.body)

        print urllib.unquote(response.url)

        self.count += 1
        print self.count,title
        box = soup.find('table', class_="infobox") 
        if box and box.find('tr') and '{{{' in box.find('tr').text: #有infobox table才分析
            self.fetch_infobox_html(title, box)
            self.parse_infobox(title, box)
