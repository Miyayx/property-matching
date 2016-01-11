#-*- coding:utf-8 -*-

from similarity import *

def generate_features(pairs, fs):
    matrix = []
    for en, zh in pairs:
        for fun in fs:
            fun(en, zh)
