import json
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])

result_set = es.search(index="news",body={
"query": {
   "bool": {
        "must": [
               { "match": { "date": "2016-02-3" } }
                      
                           ]
                              }
                               },
                                "sort" : 
                                       { "date" : {"order" : "desc"}},
                                              
                                               "size":50000,
                                                "from":0
                                                
                                                })
i=0                                                
with open('articles3.txt', 'w') as f:
    with  open('articles2.txt', 'w') as f1:
        for  hit in result_set['hits']['hits']:
            i = i+1
            print i
            c =  hit['_source']
            f.write((c['article'] + c['keywords'] +c['focus']).encode('utf-8').replace('\n',' '))
            f1.write((c['title'] + ". " +  c['keywords']).encode('utf-8').replace('\n',' '))
            f.write("\n")
            f1.write("\n")

