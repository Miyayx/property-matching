# -*- coding:utf-8 -*-

import jieba
import gensim
import math
import os
import numpy

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def cosine(v1, v2):
    cosine_similarity = numpy.dot(v1, v2)/(numpy.linalg.norm(v1)* numpy.linalg.norm(v2))
    s = cosine_similarity
    return s

def euclidean_distance(v1, v2):
    return numpy.linalg.norm(v1 - v2)

class Word2Vec:
    __metaclass__ = Singleton
    def __init__(self, model_file=None):
        import time
        start = time.time()
        print "Loading Model..."
        if model_file == None:
            model_file = os.path.join("/home/xlore/server36/BaiduWord2Vec", "baidu_corpus.model")
        self.model = gensim.models.Word2Vec.load(model_file)
        print "Load complete!"
        print "Time Consuming:", time.time()-start
    def get_vectors(self, w1, w2):
        #print w1, w2
        v1 = numpy.zeros(400)
        v2 = numpy.zeros(400)
        if w1 in self.model:
            v1 = self.model[w1]
        else:
            for w in jieba.cut(w1):
                if w in self.model:
                    v1 += self.model[w]
        if w2 in self.model:
            v2 = self.model[w2]
        else:
            for w in jieba.cut(w2):
                if w in self.model:
                    v2 += self.model[w]
        return v1, v2

    def similar(self, w1, w2): 
        v1, v2 = self.get_vectors(w1, w2)
        return cosine(v1, v2)

    def distance(self, w1, w2):
        v1, v2 = self.get_vectors(w1, w2)
        return euclidean_distance(v1, v2)

if __name__ == '__main__':
    w2v = Word2Vec(MODEL)
    print w2v.similar(u'中文名',u'英文名' )
    print w2v.similar(u'中文名',u'中文名称' )
    print w2v.similar(u'在校人数',u'在校生人数' )
    print w2v.similar(u'开工',u'开工日期' )
    print w2v.similar(u'分类等级',u'等级分类' )
    print w2v.similar(u'五笔',u'笔顺' )
    print w2v.similar(u'代表产地',u'代表产品' )

