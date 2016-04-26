#-*- coding:utf-8 -*-

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm

from fileio import *

import features
import baidu_template
import synonym
from similarity import *
import random

"""
跨语言链接
"""

import sys
sys.path.append('..')
from utils.logger import *
initialize_logger('./cross_lingual_property_matching.log')

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
            if tem in domain_dict:
                print "domain_dict %s has %d properties, no wiki property:%s"%(tem, len(domain_dict[tem].wiki_properties), p)
            continue
        try:
            #print zh_label
            zh = domain_dict[tem].baidu_properties[zh_label]
        except:
            if tem in domain_dict:
                print "domain_dict %s has %d properties, no baidu property:%s"%(tem, len(domain_dict[tem].baidu_properties), zh_label)
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

    logging.info("Positive: %d"%len(pos_properties))
    logging.info("Negative: %d"%len(neg_properties))
    logging.info("Seeds: %d"%len(seed_properties))

    # similar matrix for seeds
    #funs= [domain_similarity, value_similarity] #methods of similarity
    
    funs = []
    #funs = [popular_similarity]
    funs = [label_similarity]
    #funs = [label_similarity, popular_similarity]
    funs_cl = []
    #funs_cl = [value_similarity2]
    funs_cl = [article_similarity]
    funs_cl = [article_similarity, value_similarity2] #methods of similarity

    #funs_cl = [article_similarity] #methods of similarity
    seed_matrix = features.generate_features(seed_properties, funs, funs_cl)

    logging.info("Menthods:")
    logging.info("\t".join([fun.__name__ for fun in funs]))
    logging.info("\t".join([fun.__name__ for fun in funs_cl]))

    for i in range(seed_properties):
        p1, p2 = seed_properties[i]
        logging.info(p1.label+"\t"+p2.label+"\t"+seed_matrix[i])

    classifier = train_test(seed_matrix, seed_properties, labels)

    #for tem, domain in domain_dict.items():

    #    # for each template
    #    pairs = []
    #    for wp in domain.wiki_properties:
    #        for bp in domain.baidu_properties:
    #            pairs.append((wp, bp))
    #    matrix = features.generate_features(pairs, funs)
    #    classifier.predict(matrix)

def main_ins():
    """
    instance粒度下对齐的入口
    """
    # Read ...
    tem_ins_infobox, tem_zhins_infobox = baidu_template_article.generate_domain_articles()

    #同语言同义词合并
    #synonym.merge_baidu_synonym(domain_dict)

    # Read seeds
    seeds = read_seeds(SEEDS)
    seeds = dict(seeds)
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

    logging.info("Positive: %d"%len(pos_properties))
    logging.info("Negative: %d"%len(neg_properties))
    logging.info("Seeds: %d"%len(seed_properties))

    # similar matrix for seeds
    #funs= [domain_similarity, value_similarity] #methods of similarity
    
    funs = [label_similarity, popular_similarity]
    funs_cl = [article_similarity] #methods of similarity
    funs_cl = [article_similarity, value_similarity] #methods of similarity
    seed_matrix = features.generate_features(seed_properties, funs, funs_cl)

    logging.info("Menthods:")
    logging.info("\t".join([fun.__name__ for fun in funs]))
    logging.info("\t".join([fun.__name__ for fun in funs_cl]))

    for i in range(seed_properties):
        p1, p2 = seed_properties[i]
        logging.info(p1.label+"\t"+p2.label+"\t"+seed_matrix[i])

    classifier = train_test(seed_matrix, seed_properties, labels)

    #for tem, domain in domain_dict.items():

    #    # for each template
    #    pairs = []
    #    for wp in domain.wiki_properties:
    #        for bp in domain.baidu_properties:
    #            pairs.append((wp, bp))
    #    matrix = features.generate_features(pairs, funs)
    #    classifier.predict(matrix)

def train_test(seed_matrix, seed_properties, labels):

    print "\nLogistic Regression..."
    
    #classifier = LogisticRegression(C=1.0)
    classifier = svm.LinearSVC()
    classifier.fit(seed_matrix, labels)
    prediction =  classifier.predict(seed_matrix)
    for i, p in enumerate(seed_properties):
        print p[0].label, p[1].label, prediction[i], labels[i]
        
    print "Presicion:", classifier.score(seed_matrix, labels)
    predict_pos = 0
    actual_pos = 0
    for i in range(len(labels)):
        if prediction[i] == 1 and labels[0] == 1:
            predict_pos += 1
            actual_pos += 1
        elif labels[0] == 1:
            actual_pos += 1
    print "Recall:", predict_pos*1.0/actual_pos
    return classifier


if __name__ == '__main__':
    import time
    start = time.time()
    main_ins()
    print time.time() - start

    
