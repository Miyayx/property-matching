#-*- coding:utf-8 -*-

import sys,os,re

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

    if re.match(r'[^A-Za-z]', s):
        return True
 
    return False

def not_translate(k, v):
    if is_number(v):
        return True
    if '[[' in v and ']]' in v:
        return True
    if k == 'image':
        return True
    return False
