# -*- coding: utf-8 -*-

# Scrapy settings for template_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'template_crawler'

SPIDER_MODULES = ['template_crawler.spiders']
NEWSPIDER_MODULE = 'template_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'template_crawler (+http://www.yourdomain.com)'

WIKI='enwiki'
CONTINUE = False #是否断点续爬
URLLIB2 = False #是否使用urllib2.Request进行爬取，scrapy自带的Request容易被封
HTML = True     #是否获取html纯文本

WIKI_CONFIG = {
    'enwiki':{
        'FILE'       :'/home/keg/data/wikiraw/enwiki-template-name.dat',
        'URL_PREFIX' :'http://en.wikipedia.org/wiki/',
        'OUTPUT'     :'/home/keg/data/infobox/enwiki-template-label-scrapy.dat',
        'HTML_OUTPUT':'/home/keg/data/infobox/enwiki-template-html-scrapy.dat',
        'fail-404'   :'./log/enwiki-404.dat'
    },
    'zhwiki':{
        'FILE'       :'/home/keg/data/wikiraw/zhwiki-template-name.dat',
        'URL_PREFIX' :'http://zh.wikipedia.org/zh-cn/',
        'OUTPUT'     :'/home/keg/data/infobox/zhwiki-template-label-scrapy.dat',
        'HTML_OUTPUT':'/home/keg/data/infobox/zhwiki-template-html-scrapy.dat',
        'fail-404'   :'./log/zhwiki-404.dat'
    }
}
