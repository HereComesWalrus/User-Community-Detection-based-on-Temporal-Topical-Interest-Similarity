import logging
from gensim import corpora
import gensim
import os
from gensim.models.ldamulticore import LdaMulticore
from gensim.matutils import cossim
import string
import pyLDAvis
from pyLDAvis import gensim
import numpy as np
import networkx as nx
import community
from scipy.linalg import norm
from scipy.spatial.distance import euclidean


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64

def hellinger1(p, q):
    return norm(np.sqrt(p) - np.sqrt(q)) / _SQRT2

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


with open('annotatedEntities.txt', 'r') as f:
    documents = [line.translate(None, string.punctuation.replace("_","")).strip() for line in f]

stoplist = set('for a of the and to in , en'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]for document in documents]

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/tweets_sample.dict')
	
corpus = [dictionary.doc2bow(text) for text in texts]

lda = LdaMulticore.load("multicoreLDA")

doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in lda[corpus]])
doc_topic_dist.shape

UserGraph = nx.Graph()
UserGraph.add_nodes_from([0, len(doc_topic_dist)])

for docIndex in range(len(doc_topic_dist)):
  for compareIndex in range(docIndex+1,len(doc_topic_dist)):
    hellinger = hellinger1(doc_topic_dist[docIndex],doc_topic_dist[compareIndex]) 
    if hellinger<0.2:
       UserGraph.add_edge(docIndex, compareIndex, weight=hellinger)
       print UserGraph[docIndex][compareIndex]

nx.write_gml(UserGraph, "usergraph.gml.gz")