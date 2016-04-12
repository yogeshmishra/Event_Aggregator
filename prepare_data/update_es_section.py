import json
from collections import Counter
import math
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'}])
basefolder = 'input/'

def updateES(ESClient=Elasticsearch(), idfilename=basefolder+"ids.txt", bCategoryFilename=basefolder+"sections.txt"):
    if sum(1 for line in open(bCategoryFilename,"r")) != sum(1 for line in open(idfilename,"r")):
        print "LINE MISMATCH ERROR "
        return 
    with open(idfilename,"r") as idfile, open(bCategoryFilename,"r") as bCategoryfile:
        line = 0
        while True:
            try:
                line +=1
                id , section = next(idfile),next(bCategoryfile)
                id = id.strip()
                section = section.strip()
                print id,section 
                update_data(ESClient, id, section)
            except Exception as e:
                print "READ ERROR : LINE ", line, str(e)
                break
    
def update_data(Client, id, section):
    Client.update(index="jan_news", doc_type="articles", id=id, body={"doc":{"section":section}})

if __name__=="__main__":
    updateES(ESClient=es)
