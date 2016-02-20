#-*- coding:utf-8 -*-

import numpy as np
from sklearn.linear_model import LogisticRegression

from fileio import *

import features
import baidu_template
import synonym
from similarity import *
import random

"""

"""
def main():
    # Read ...
    domain_dict = baidu_template.generate_domain_properties()

    #同语言同义词合并
    #synonym.merge_baidu_synonym(domain_dict)

    # Read seeds
    seeds = read_seeds(SEEDS)
    pos_properties = []
    neg_properties = []
    labels = []
    for en_label, zh_label in seeds:
        tem, p = en_label.split('\t')
        for k in domain_dict[tem].baidu_properties.keys():
            print k
        try:
            en = domain_dict[tem].wiki_properties[p]
        except:
           print "domain_dict has no wiki property:", p
           continue
        try:
           print zh_label
           zh = domain_dict[tem].baidu_properties[zh_label]
        except:
           print "domain_dict has no baidu property:", zh_label
           continue
        pos_properties.append((en, zh))
        labels.append(1)
        zh2 = random.sample(domain_dict[tem].baidu_properties.items(), 1)[0][1] #注意这里返回random的是一个item的list
        if zh2.label != zh_label:
            neg_properties.append((en, zh2))
            labels.append(0)
        en2 = random.sample(domain_dict[tem].wiki_properties.items(), 1)[0][1]
        if en2.label != en_label:
            neg_properties.append((en2, zh))
            labels.append(0)

    seed_properties = pos_properties[:10] + neg_properties[:10]
    print "Seeds:",len(seed_properties)

    # similar matrix for seeds
    #funs= [domain_similarity, value_similarity] #methods of similarity
    funs= [value_similarity] #methods of similarity
    seed_m = features.generate_features(seed_properties, funs)
    print seed_m

    #labels = [p[0].label+p[1].label for p in seed_properties]
    print "Logistic Regression..."
    classifier = LogisticRegression(C=1.0)
    classifier.fit(seed_m, labels)
    print classifier.score(seed_m, labels)

    #for tem, domain in domain_dict.items():

    #    # for each template
    #    pairs = []
    #    for wp in domain.wiki_properties:
    #        for bp in domain.baidu_properties:
    #            pairs.append((wp, bp))
    #    matrix = features.generate_features(pairs, funs)
    #    classifier.predict(matrix)

if __name__ == '__main__':
    main()

    
