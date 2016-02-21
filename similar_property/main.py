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
    seed_properties = []
    tems = set()
    for en_label, zh_label in seeds:
        tem, p = en_label.split('\t')
        tems.add(tem)
        try:
            en = domain_dict[tem].wiki_properties[p]
        except:
           print "domain_dict %s has no wiki property:%s"%(tem, p)
           continue
        try:
           #print zh_label
           zh = domain_dict[tem].baidu_properties[zh_label]
        except:
           print "domain_dict %s has no baidu property:%s"%(tem, zh_label)
           continue
        pos_properties.append((en, zh))
        zh2 = random.sample(domain_dict[tem].baidu_properties.items(), 1)[0][1] #注意这里返回random的是一个item的list
        if zh2.label != zh_label:
            neg_properties.append((en, zh2))
            continue
        en2 = random.sample(domain_dict[tem].wiki_properties.items(), 1)[0][1]
        if en2.label != en_label:
            neg_properties.append((en2, zh))

    #for tem in tems:
    #    print "Template:",tem
    #    for k in domain_dict[tem].baidu_properties.keys():
    #        print k

    #seed_properties = pos_properties[:10] + neg_properties[:10]
    seed_properties = pos_properties + neg_properties
    labels = [1] * len(pos_properties) + [0] * len(neg_properties)

    print "Positive:", len(pos_properties)
    print "Negative:", len(neg_properties)
    print "Seeds:",len(seed_properties)

    # similar matrix for seeds
    #funs= [domain_similarity, value_similarity] #methods of similarity
    
    funs = [label_similarity, popular_similarity]
    #funs_cl = [article_similarity, value_similarity] #methods of similarity
    funs_cl = [article_similarity] #methods of similarity
    seed_matrix = features.generate_features(seed_properties, funs, funs_cl)
    print seed_matrix

    #labels = [p[0].label+p[1].label for p in seed_properties]
    print "\nLogistic Regression..."
    
    classifier = LogisticRegression(C=1.0)
    classifier.fit(seed_matrix, labels)
    prediction =  classifier.predict(seed_matrix)
    for i, p in enumerate(seed_properties):
        print p[0].label, p[1].label, prediction[i], labels[i]
        
    print classifier.score(seed_matrix, labels)

    #for tem, domain in domain_dict.items():

    #    # for each template
    #    pairs = []
    #    for wp in domain.wiki_properties:
    #        for bp in domain.baidu_properties:
    #            pairs.append((wp, bp))
    #    matrix = features.generate_features(pairs, funs)
    #    classifier.predict(matrix)

if __name__ == '__main__':
    import time
    start = time.time()
    main()
    print time.time() - start

    
