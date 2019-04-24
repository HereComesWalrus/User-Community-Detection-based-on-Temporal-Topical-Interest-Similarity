import logging
from gensim import corpora
import gensim
import os
from gensim.models.ldamulticore import LdaMulticore
import string
import pyLDAvis
from pyLDAvis import gensim
import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open('annotatedEntities.txt', 'r') as f:
    documents = [line.translate(None, string.punctuation.replace("_","")).strip() for line in f]

stoplist = set('for a of the and to in , en'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]for document in documents]

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/tweets_sample.dict')
	
corpus = [dictionary.doc2bow(text) for text in texts]

start = time.time()

model = LdaMulticore(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=18, 
                                           chunksize=300,passes=50, minimum_probability=0.0, per_word_topics=False)

end = time.time()
print("Time taken creating and training the LDA distribution model: ")
print(end - start)

model.save("multicoreLDA")

data = pyLDAvis.gensim.prepare(model, corpus, dictionary, mds='pcoa', R=10)
pyLDAvis.show(data)