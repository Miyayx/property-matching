#-*- coding:utf-8 -*-
import os
DIR = '/Users/Miyayx/server36'
import six
print  six.__version__
import gensim

# import modules and set up logging
from gensim.models import word2vec
# load up unzipped corpus from http://mattmahoney.net/dc/text8.zip
#sentences = word2vec.Text8Corpus(os.path.join(DIR, 'word2vec/text'))
sentences = [l for l in open(os.path.join(DIR, 'word2vec/text'))]
# train the skip-gram model; default window=5
model = word2vec.Word2Vec(sentences, size=200)
# ... and some hours later... just as advertised...
model.most_similar(positive=['姓名'], negative=['man'], topn=10)

## pickle the entire model to disk, so we can load&resume training later
#model.save(os.path.join(DIR, 'word2vec/text.model'))
## store the learned weights, in a format the original C tool understands
#model.save_word2vec_format('/tmp/text8.model.bin', binary=True)
## or, import word weights created by the (faster) C word2vec
## this way, you can switch between the C/Python toolkits easily
#model = word2vec.Word2Vec.load_word2vec_format('/tmp/vectors.bin', binary=True)
## "boy" is to "father" as "girl" is to ...?
#model.most_similar(['girl', 'father'], ['boy'], topn=3) [('mother', 0.61849487), ('wife', 0.57972813), ('daughter', 0.56296098)]
#more_examples = ["he his she", "big bigger bad", "going went being"]
