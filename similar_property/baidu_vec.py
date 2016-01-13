# -*- coding:utf-8 -*-

import jieba
import gensim
import math
import os
import numpy

DIR="/home/xlore/server36/BaiduWord2Vec/"
MODEL=os.path.join(DIR, "baidu_corpus.model")

def cosine(v1, v2):
    cosine_similarity = numpy.dot(v1, v2)/(numpy.linalg.norm(v1)* numpy.linalg.norm(v2))
    return cosine_similarity

class Word2Vec:
    def __init__(self, model_file):
        import time
        start = time.time()
        self.model = gensim.models.Word2Vec.load(model_file)
        print "Load complete!"
        print "Time Consuming:", time.time()-start

    def similar(self, w1, w2):
        print w1, w2
        v1 = numpy.zeros(400)
        v2 = numpy.zeros(400)
        if w1 in self.model:
            v1 = self.model[w1]
        else:
            for w in jieba.cut(w1):
                v1 += self.model[w]
        if w2 in self.model:
            v2 = self.model[w2]
        else:
            for w in jieba.cut(w2):
                v2 += self.model[w]
        return cosine(v1, v2)


if __name__ == '__main__':
    w2v = Word2Vec(MODEL)
    print w2v.similar(u'中文名',u'英文名' )
    print w2v.similar(u'中文名',u'中文名称' )
    print w2v.similar(u'在校人数',u'在校生人数' )
    print w2v.similar(u'开工',u'开工日期' )
    print w2v.similar(u'分类等级',u'等级分类' )
    print w2v.similar(u'五笔',u'笔顺' )
    print w2v.similar(u'代表产地',u'代表产品' )

