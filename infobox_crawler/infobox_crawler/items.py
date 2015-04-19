# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfoboxCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    prop = scrapy.Field()
    value = scrapy.Field()
