import sys

from gensim import corpora, models, similarities                               
fileList = ['non_ners.txt', 'locations.txt', 'persons.txt', 'enriched_keys.txt']

for filename in fileList:
    dictionary = corpora.Dictionary.load('/tmp/' + filename.strip('.txt')+'.dict')
    corpus = corpora.MmCorpus('/tmp/' + filename.strip('.txt')+ '.mm')

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]
    index = similarities.MatrixSimilarity(corpus_tfidf)
    index.save('/tmp/' + filename.strip('.txt')+ '.index')
    index = similarities.MatrixSimilarity.load('/tmp/' + filename.strip('.txt')+ '.index')

    sims = index[corpus_tfidf]
    with open('output_'+filename, 'w') as out:
        for s in sims:
            outlist = sorted(list(enumerate(s)),key=lambda x: x[1], reverse=True)[:6]
            out.write(unicode(outlist))
            out.write('\n')

