import sys

from gensim import corpora, models, similarities                               
dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
corpus = corpora.MmCorpus('/tmp/deerwester.mm')

tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]
index = similarities.MatrixSimilarity(corpus_tfidf)
index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[corpus_tfidf]
#print(list(enumerate(sims)))
print sims
print("Sortedp--------------------->")
for s in sims:
    outlist = sorted(list(enumerate(s)),key=lambda x: x[1], reverse=True)[:4]
    print outlist
