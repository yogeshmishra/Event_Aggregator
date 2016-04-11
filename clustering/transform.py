import sys

from gensim import corpora, models, similarities                               
dictionary = corpora.Dictionary.load('/tmp/news_articles.dict')
corpus = corpora.MmCorpus('/tmp/news_articles.mm')

tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]
index = similarities.MatrixSimilarity(corpus_tfidf)
index.save('/tmp/news_articles.index')
index = similarities.MatrixSimilarity.load('/tmp/news_articles.index')

sims = index[corpus_tfidf]
#print(list(enumerate(sims)))
print sims
print("Sortedp--------------------->")
for s in sims:
    outlist = sorted(list(enumerate(s)),key=lambda x: x[1], reverse=True)[:6]
    print outlist
