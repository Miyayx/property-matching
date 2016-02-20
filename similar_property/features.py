#-*- coding:utf-8 -*-

from similarity import *
from fileio import *

import numpy as np

def generate_features(pairs, fs=[], fs_cl=[]):
    """
    """
    print "Generating features..."
    cl = read_crosslingual(WIKI_CROSSLINGUAL)
    n, m = len(pairs), len(fs)+len(fs_cl)
    matrix = np.zeros((n,m))
    for i, pair in enumerate(pairs):
        en, zh = pair
        print "Features for:",en.label,zh.label
        for j, fun in enumerate(fs):
            res = fun(en, zh)
            print res
            matrix[i][j] = res

    for i, pair in enumerate(pairs):
        en, zh = pair
        print "Features for:",en.label,zh.label
        for j, fun in enumerate(fs_cl):
            res = fun(en, zh, cl)
            print res
            matrix[i][j+len(fs)] = res
    return matrix
