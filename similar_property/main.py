#-*- coding:utf-8 -*-

import numpy as np
from sklearn.linear_model import LogisticRegression

from fileio import *

import features
import baidu_template
import synonym
from similarity import *

"""

"""
def main():
    # Read ...
    domain_dict = baidu_template.generate_domain_properties()

    synonym.merge_baidu_synonym(domain_dict)

    # Read seeds
    seeds = read_seeds()
    pos_properties = []
    neg_properties = []
    for en_label, zh_label in seeds:
        tem, p = en_label.split('\t')
        en = domain_dict[tem].wiki_properties[p]
        zh = domain_dict[tem].baidu_properties[zh_label]
        pos_properties.append((en, zh))
        zh2 = random.sample(domain_dict[tem].baidu_properties, 1)
        if zh2.label != zh_label:
            neg_properties.append((en, zh2))
        en2 = random.sample(domain_dict[tem].wiki_properties, 1)
        if en2.label != en_label:
            neg_properties.append((en2, zh))

    # similar matrix for seeds
    funs= [] #methods of similarity
    seed_m = features.generate_features(seed_properties, funs)
    labels = []

    classifier = LogisticRegression(C=1.0)
    classifier.fit(seed_m, labels)

    for tem, domain in domain_dict.items():

        # for each template
        pairs = []
        for wp in domain.wiki_properties:
            for bp in domain.baidu_properties:
                pairs.append((wp, bp))
        matrix = features.generate_features(pairs, funs)
        classifier.predict(matrix)

if __name__ == '__main__':
    main()

    
