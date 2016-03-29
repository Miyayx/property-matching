# !/bin/python
# -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN

import os
import sys
import random

sys.stdout = open("output-dbscan","w")

def read_properties(fn):
    d = {}
    for line in open(fn):
        doc, text = line.strip('\n').split('\t')
        props = [t.split(':::')[0] for t in text.split('::;')]
        d[doc] = props
    return d

def read_concepts(fn):
    d = {}
    for line in open(fn):
        doc, text = line.strip('\n').split('\t')
        cons = text.split(';')
        d[doc] = cons
    return d

def generate_segs(d1, d2):
    for k, v in d2.iteritems():
        if k in d1:
            d1[k] += d2[k]
    for k, v in d1.iteritems():
        d1[k] = ' '.join(v)
    return d1

if __name__ == '__main__':
    DIR = '/Users/Miyayx/server36/'
    doc_props = read_properties(os.path.join(DIR, 'taxonomy/baidu-title-property.dat'))
    print len(doc_props)
    doc_cons = read_concepts(os.path.join(DIR, 'taxonomy/baidu-instance-concept.dat'))
    print len(doc_cons)
    doc_segs = generate_segs(doc_props, doc_cons)
    doc_segs = random.sample(doc_segs.items(), 50000)
    #doc_segs = sorted(doc_segs.iteritems())
    
    del doc_props

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([ds[1] for ds in doc_segs])
    print tfidf_matrix
    #cosine = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

    #cluster = KMeans(n_clusters=1000, init='k-means++', max_iter=100, n_init=1)
    cluster = DBSCAN(eps=0.2, min_samples=10, metric='euclidean', algorithm='auto', leaf_size=30, p=None, random_state=None)
    cluster.fit(tfidf_matrix)

    res = {}
    for i, l in enumerate(cluster.labels_):
        if not l in res:
            res[l] = []
        res[l].append(doc_segs[i][0])

    for c, docs in res.iteritems():
        print "cluster ",c
        con_count = {}
        for doc in docs:
            if doc in doc_cons:
                for c in doc_cons[doc]:
                    con_count[c] = con_count.get(c, 0) + 1
        for c in sorted(con_count.items(), key=lambda x:x[1], reverse=True)[:3]:
            print c[0], c[1]
        print ' '.join(docs)



