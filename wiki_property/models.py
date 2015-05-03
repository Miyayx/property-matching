#!/usr/bin/python
# -*- coding:utf-8 -*-

class PageProperty:

    prop_label = ''  #属性名称，即显示在网页上的文本
    link_label = ''  #如果在网页中有链接的话，链接指向的article label
    value = ''  #网页中爬取的value值

    def __init__(self, pl, ll, v):
        self.prop_label = pl
        self.link_label = ll
        self.value = v

class DumpProperty:
    dump_label = ''  #dump文件中的属性名称，可能是template属性
    value = ''  #dump文件中的value值

    def __init__(self, l, v=''):
        self.dump_label = l
        self.value = v

class Property:
    """
    PageProperty和DumpProperty对齐后的产物，只保留page上有的，不保留dump多出来的property
    """
    prop_label = ''  #属性名称，即显示在网页上的文本
    link_label = ''  #如果在网页中有链接的话，链接指向的article label
    dump_label = ''  #dump文件中的属性名称，可能是template属性
    value = ''       #dump文件中的value值, 爬取的value值只是用来对应同语言下的property的，之后就没有用了

    def __init__(self, pl, ll, dl, v):
        self.prop_label = pl
        self.link_label = ll
        self.dump_label = dl
        self.value = v
        self.matched = False

class Infobox:

    title = '' # article title
    props = []

    def __init__(self, t):
        self.title = t
        self.props = []

class MatchedInfobox:

    title = {'en':'', 'zh':''}
    m_props = []
    en_props = []  # Property List
    zh_props = []  # Property List

    def __init__(self, en, zh):
        self.title = {'en':en, 'zh':zh}
        self.m_props = []
        self.en_props = []  # Property List
        self.zh_props = []  # Property List


