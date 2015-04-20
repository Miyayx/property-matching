# -*- coding: utf-8 -*-

# Scrapy settings for infobox_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'infobox_crawler'

SPIDER_MODULES = ['infobox_crawler.spiders']
NEWSPIDER_MODULE = 'infobox_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'infobox_crawler (+http://www.yourdomain.com)'

WIKI='zhwiki'
CONTINUE = True #是否断点续爬

WIKI_CONFIG = {
    'enwiki':{
        'FILE'      :'/home/keg/data/wikiraw/enwiki-infobox-tmp.dat',
        'URL_PREFIX':'http://en.wikipedia.org/wiki/',
        'OUTPUT'    :'/home/keg/data/infobox/enwiki-infobox-scrapy.dat'
    },
    'zhwiki':{
        'FILE'      :'/home/keg/data/wikiraw/zhwiki-infobox-tmp.dat',
        'URL_PREFIX':'http://zh.wikipedia.org/zh-cn/',
        'OUTPUT'    :'/home/keg/data/infobox/zhwiki-infobox-scrapy.dat'
    }
}


