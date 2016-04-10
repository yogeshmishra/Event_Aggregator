import json
from collections import Counter
import math
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'}])
basefolder = 'output/outputFiles/'

topic_names={}

def getTopicNames(filename=basefolder+"topicNames.txt"):
    print "##############################################"
    print "READING " + filename + " "
    with open(filename,"r") as topicname:
        for line in topicname:
            elements = line.split("|")
            key = elements[0].strip()
            value = elements[1].strip()
            if value == "IGNORE":
                continue

            topic_names[key] = value

def updateES(ESClient=Elasticsearch(), idfilename=basefolder+"id.txt", topicfilename=basefolder+"topics.txt", keywordsfilename=basefolder+"corpus.txt"):
    if sum(1 for line in open(topicfilename)) != sum(1 for line in open(idfilename)):
        print "LINE MISMATCH ERROR "
        return 
    with open(idfilename,"r") as idfile, open(topicfilename,"r") as topicfile, open(keywordsfilename, "r") as keywordsfile:
        line = 0
        while True:
            try:
                line +=1
                id , topics, keywords = next(idfile),next(topicfile), next(keywordsfile)
                id = id.strip()
                topics= filter(None,topics.split(','))
                topicCounter = Counter(topics) 
                total = sum(topicCounter.values(),0.0)
                for key in topicCounter:
                    topicCounter[key] /=total

                topicCounter = dict(topicCounter)
                
                topics = {}
                for key in topicCounter:
                    try:
                        topics[ topic_names[key] ] = topicCounter[key]
                    except:
                        pass
                print id , topics
                print keywords
                update_data(ESClient, id, topics, keywords)
            except Exception as e:
                print "READ ERROR : LINE ", line, str(e)
                break
    
def update_data(Client, id, topics, keywords):
    Client.update(index="news", doc_type="articles", id=id, body={"doc":{"topics":topics, "enriched_keywords":keywords}})
if __name__=="__main__":
    getTopicNames(filename=basefolder+ "topicNames.txt")
    updateES(ESClient=es)
