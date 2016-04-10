# -*- coding:utf-8 -*-
import re

def clean_label(label):
    replaceds = re.findall(r'\[\[.+?\]\]', label)
    replaces  = re.findall(r'\[\[(.+?)\]\]', label)
    
    for i in range(len(replaces)):
        label = label.replace(replaceds[i], replaces[i].split('|')[-1])
    return label
   
