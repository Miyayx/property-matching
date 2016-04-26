# -*- coding:utf-8 -*-
import os
import codecs

from similarity import *
from fileio import *

import numpy as np


def cluster(X):
    
    from sklearn.cluster import DBSCAN
    from sklearn import metrics
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.preprocessing import StandardScaler

    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=1).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print('Estimated number of clusters: %d' % n_clusters_)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f"
                  % metrics.adjusted_mutual_info_score(labels_true, labels))
    print("Silhouette Coefficient: %0.3f"
                  % metrics.silhouette_score(X, labels))

def compare(p1, p2, cl):
    """
    对比两个property
    1. label edit distance
    2. 不同时出现在同一个文章
    3. value 对比: 文本，数字，日期
    """
    #similarities = [label_similarity, valuesimilarity_number, valuesimilarity_date, range_similarity]
    funs = [label_similarity]
    funs_cl = [value_similarity2]
    #similarities = [label_similarity, value_similarity2]
    print "Compare:",p1.label, p2.label
    result = []
    for fun in funs:
        r = fun(p1, p2)
        print fun.__name__, r
        result.append(r)

    for fun in funs_cl:
        r = fun(p1, p2, cl)
        print fun.__name__, r
        result.append(r)

    #print "label:", edit_distance_similarity(p1.label, p2.label)
    #print "reversed_articel_similarity", reversed_article_similarity(p1, p2)
    #print "valuesimilarity_number", valuesimilarity_number(p1, p2)
    #print "valuesimilarity_date", valuesimilarity_date(p1, p2)
    #print "valuesimilarity_literal", valuesimilarity_literal(p1, p2)
    return sum(result)/len(result)

def merge_baidu_synonym(domain_dict):

    for tem, domain in domain_dict.items():
        bps = domain.baidu_properties.values()
        cluster = {}
        cluster2 = {}
        for bp1 in bps:
            for bp2 in bps:
                if bp1 == bp2:
                    continue
                c = compare(bp1, bp2)
                # 还差合并的代码


def main():
    
    d = read_baidu_properties(BAIDU_INFOBOX)
    cl = read_crosslingual(WIKI_CROSSLINGUAL)

    for line in codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE+"4-2", 'r', 'utf-8'):
        tem, attributes = line.strip('\n').split('\t',1)
        attrs = attributes.strip(':::').split(':::')
 
        print "Template:", tem, len(attrs)
        X = np.zeros((len(attrs),len(attrs)))
 
        for i in range(len(attrs)):
            if not attrs[i] in d:
                continue
            p1 = d[attrs[i]]
            for j in range(i+1, len(attrs)):
                #print attrs[i], attrs[j], compare(d[attrs[i]], d[attrs[j]])
                if attrs[i] in d and attrs[j] in d:
                    p2 = d[attrs[j]]
                    c = compare(p1, p2, cl)
                    X[i][j] = c
                    X[j][i] = c
            #            if c > Max[1]:
            #                Max = (p2, c)
            #if not Max[0] == None:
            #    print "Most similar:", p1.label, Max[0].label, Max[1] 
 
        cluster(X)

if __name__ == '__main__':
    main()
    
