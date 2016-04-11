from gensim import corpora, models, similarities
import sys
import ast

baseFolder="../data/"

fileList = ['non_ners.txt', 'locations.txt', 'persons.txt', 'enriched_keys.txt']

def MyCorpus(dictionaryi, fileName):
    for line in open(baseFolder+filename):
        # assume there's one document per line, tokens separated by whitespace
        yield dictionary.doc2bow(ast.literal_eval(line))


for filename in fileList:
    dictionary = corpora.Dictionary( ast.literal_eval(line) for line in open(baseFolder+ filename))
    dictionary.save('/tmp/' + filename.strip('.txt') +'.dict') # store the dictionary, for future reference
    print dictionary

    corpus = MyCorpus(dictionary, filename)
    corpora.MmCorpus.serialize('/tmp/' + filename.strip('.txt') +'.mm', corpus)
