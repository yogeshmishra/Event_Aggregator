from gensim import corpora, models, similarities
import sys
import ast

baseFolder="../data/"
def createText(file):
    text =[]
    with open(baseFolder+"non_ners.txt", 'r')  as non_ners:
        for line in  non_ners:
            line = ast.literal_eval(line)
            text.append(line)
    return text

def MyCorpus(dictionary):
    for line in open(baseFolder+'non_ners.txt'):
        # assume there's one document per line, tokens separated by whitespace
        yield dictionary.doc2bow(ast.literal_eval(line))


dictionary = corpora.Dictionary( ast.literal_eval(line) for line in open(baseFolder+'non_ners.txt'))
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print dictionary

corpus_memory_friendly = MyCorpus(dictionary)
corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus_memory_friendly)
