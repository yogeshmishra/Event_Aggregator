from pprint import pprint
import json
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])
count =0
idMap={}
with open('ids.txt','r') as r:
    for l in r:
        idMap[count]=l.strip()
        count+=1

while True:
    doc = int(raw_input("Doc id "))
    if doc== -1:
        break
    
    result  = es.get(index="jan_news", doc_type='articles', id=idMap[doc])
    #print result

    pprint( result )

