import json
import sys
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])
basefolder = 'rawFiles/'
def create_lda_input_files(size=5000, filename="articles.txt"):
    from_value=0
    total=1
    i=0                                                
    while total > from_value:
        result_set = es.search(index="news",body={
        "query": {
           "bool": {
                "must": [
                       { "match": { "month": 12 } },
                       {"match": {"year":2015}}
                              
                                   ]
                                      }
                                       },
                                        "sort" : 
                                               { "date" : {"order" : "desc"}},
                                                      
                                                       "size":size,
                                                        "from":from_value
                                                        
                                                        })
        total=result_set['hits']['total']
        from_value=from_value + size
        with open(filename, 'a') as f:
            with  open(basefolder+'articles2.txt', 'a') as f1:
                for  hit in result_set['hits']['hits']:
                    i = i+1
                    print i, hit['origin'], hit['date']
                    c =  hit['_source']
                    f1.write((c['article'] + c['keywords'] +c['focus']).encode('utf-8').replace('\n',' '))
                    f.write((c['title'] + ". " +  c['keywords'] + ". "+ c['focus']).encode('utf-8').replace('\n',' '))
                    f.write("\n")
                    f1.write("\n")

if __name__=="__main__":
    s = 5000
    f="articles.txt"
    if len(sys.argv) == 3:
        s = int(sys.argv[1])
        f= sys.argv[2]
    elif len(sys.argv)==2:
        s = int(sys.argv[1])
        
    create_lda_input_files(size=s,filename=basefolder+f)
