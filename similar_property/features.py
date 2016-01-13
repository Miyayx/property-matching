#-*- coding:utf-8 -*-

from similarity import *
from fileio import *

def generate_features(pairs, fs):
    cl = read_crosslingual(WIKI_CROSSLINGUAL)
    matrix = []
    for en, zh in pairs:
        for fun in fs:
            fun(en, zh, cl)
