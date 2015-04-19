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

ENWIKI_FILE = ''
ZHWIKI_FILE = '' 
ENWIKI_URL = "http://en.wikipedia.org/wiki/"
ZHWIKI_URL = "http://zh.wikipedia.org/zh-cn/"
ENWIKI_OUTPUT = ''
ZHWIKI_OUTPUT = ''

