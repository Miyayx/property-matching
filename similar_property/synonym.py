# -*- coding:utf-8 -*-
import os
import codecs

from similarity import *
from fileio import *

import numpy as np
from baidu_vec import Word2Vec

from sklearn.preprocessing import normalize

def cluster(X, attrs):
    
    from sklearn.cluster import DBSCAN
    from sklearn import metrics
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.preprocessing import StandardScaler

    # Compute DBSCAN
    db = DBSCAN(eps=0.4, min_samples=1, metric='precomputed').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    d = {}
    for i in range(len(attrs)):
        #print attrs[i],labels[i]
        if not labels[i] in d:
            d[labels[i]] = []
        d[labels[i]].append(attrs[i])
    
    for c, ats in sorted(d.iteritems(), key=lambda x:x[0]):
        if len(ats) > 1:
            print c, (",".join(ats)).encode('utf-8')
    
    print('Estimated number of clusters: %d' % n_clusters_)
    #print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    #print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    #print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    #print("Adjusted Rand Index: %0.3f"
    #      % metrics.adjusted_rand_score(labels_true, labels))
    #print("Adjusted Mutual Information: %0.3f"
    #              % metrics.adjusted_mutual_info_score(labels_true, labels))
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
    w2v = Word2Vec()
    funs = [label_similarity]
    funs_cl = [value_similarity2]
    #similarities = [label_similarity, value_similarity2]
    #print "Compare:",p1.label, p2.label
    result = []
    #for fun in funs:
    #    r = fun(p1, p2)
    #    #print fun.__name__, r
    #    result.append(r)

    #for fun in funs_cl:
    #    r = fun(p1, p2, cl)
    #    #print fun.__name__, r
    #    result.append(r)
    #d_label = edit_distance(p1.label, p2.label)
    d_label = jaccard_distance(p1.label, p2.label)
    result.append(d_label)
   
    d_v = 1-value_similarity2(p1, p2, cl)
    result.append(d_v)

    d_w2v = w2v.distance(p1.label, p2.label)
    #print "word2vec:",w2v_sim
    result.append(d_w2v)

    #print "label:", edit_distance_similarity(p1.label, p2.label)
    #print "reversed_articel_similarity", reversed_article_similarity(p1, p2)
    #print "valuesimilarity_number", valuesimilarity_number(p1, p2)
    #print "valuesimilarity_date", valuesimilarity_date(p1, p2)
    #print "valuesimilarity_literal", valuesimilarity_literal(p1, p2)
    return sum(result)/len(result), result

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

def main(matrix_file = None):

    if matrix_file:
        X, attrs = read_matrix(matrix_file)
        cluster(X, attrs)
    else:
        generate_matrx()

def read_matrix(fn):
    results = []
    attrs = []
    for line in codecs.open(fn, 'r', 'utf-8'):
        try:
            p1, p2, ms = line.strip('\n').split('\t')
        except:
            print line 
            continue
        if not p1 in attrs:
            attrs.append(p1)
        result = [float(m) for m in ms.split(',')]
        results.append(result)

    X = np.zeros((len(attrs),len(attrs)))
   
    #没种距离归一化
    results = normalize(np.array(results))
    print results

    k = 0
    for i in range(len(attrs)):
        for j in range(i, len(attrs)):
            #print attrs[i].encode('utf-8'),attrs[j].encode('utf-8'),results[k]
            X[i][j] = sum(results[k])/len(results[k])
            X[j][i] = X[i][j]
            k += 1
    return X, attrs
    
def generate_matrx():
    #templates = ["Template:Infobox film","Template:Infobox company","Template:Infobox single"]
    templates = ["Template:Infobox film"]

    d = read_baidu_properties(BAIDU_INFOBOX)
    cl = read_crosslingual(WIKI_CROSSLINGUAL)

    fw = codecs.open('dbscan_matrix.dat', 'w', 'utf-8')

    for line in codecs.open(ENWIKI_TEMPLATE_BAIDU_ATTRIBUTE+"4-2", 'r', 'utf-8'):
        tem, attributes = line.strip('\n').split('\t', 1)
        if not tem in templates:
            continue
        attrs = attributes.strip().strip(':::').split(':::')
        attrs = [a for a in attrs if a in d and len(a) > 0]
 
        fw.write(tem+'\n')
        fw.flush()
        print "Template:", tem, len(attrs)
        X = np.zeros((len(attrs),len(attrs)))
        results = []
 
        for i in range(len(attrs)):
            p1 = d[attrs[i]]
            for j in range(i, len(attrs)):
                #print attrs[i], attrs[j], compare(d[attrs[i]], d[attrs[j]])
                p2 = d[attrs[j]]
                c, result = compare(p1, p2, cl)
                fw.write('%s\t%s\t%s\n'%(p1.label, p2.label, ",".join([str(r) for r in result])))
                fw.flush()
                results.append(result)
                #X[i][j] = c
                #X[j][i] = c
            #            if c > Max[1]:
            #                Max = (p2, c)
            #if not Max[0] == None:
            #    print "Most similar:", p1.label, Max[0].label, Max[1] 

        #没种距离归一化
        results = normalize(np.array(results))
        print results

        k = 0
        for i in range(len(attrs)):
            for j in range(i, len(attrs)):
                X[i][j] = sum(results[k])/len(results[k])
                X[j][i] = X[i][j]
                k += 1
        
        cluster(X, attrs)
 

if __name__ == '__main__':
    import time
    start = time.time()
    main('dbscan_matrix.dat')
    #main()
    print "Time Consuming:",time.time()-start
    
