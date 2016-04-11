import sys

from gensim import corpora, models, similarities                               
baseFolder ="results/"
fileList = ['non_ners.txt', 'locations.txt', 'persons.txt', 'enriched_keys.txt']
sims ={}
for filename in fileList:
    dictionary = corpora.Dictionary.load('/tmp/' + filename.strip('.txt')+'.dict')
    corpus = corpora.MmCorpus('/tmp/' + filename.strip('.txt')+ '.mm')

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]
    index = similarities.MatrixSimilarity(corpus_tfidf)
    index.save('/tmp/' + filename.strip('.txt')+ '.index')
    index = similarities.MatrixSimilarity.load('/tmp/' + filename.strip('.txt')+ '.index')

    sims[filename] = index[corpus_tfidf]

fileListRemoved = [ 'locations.txt', 'persons.txt', 'enriched_keys.txt']

mainFile = 'non_ners.txt' 
results = [[ 0.0 for i in range(len(sims[mainFile][0]))] for j in range(len(sims[mainFile]))]
print results
for key in fileList:
    sim = sims[key]
    #print key
    for i in range(len(sim)):
        #print sims[mainFile][i][:5], sim[i][:5]
        #print  [ x + y for x,y in zip(results[i],sim[i])][:5]
        results[i] = [ x + y for x,y in zip(results[i],sim[i])]
        #print results[i]
aggSim = results

with open("output.txt","w") as out:
    for s in aggSim:
        outlist = sorted(list(enumerate(s)),key=lambda x: x[1], reverse=True)[:6]
        out.write(unicode(outlist))
        out.write('\n')

