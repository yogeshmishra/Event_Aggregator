import json
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])

def create_lda_input_files(size=5000, filename="articles.txt"):
    from_value=0
    total=1
    i=0                                                
    while total > from_value:
        result_set = es.search(index="news",body={
        "query": {
           "bool": {
                "must": [
                       #{ "match": { "month": "2" } },
                       {"match": {"year":2016}}
                              
                                   ]
                                      }
                                       },
                                        "sort" : 
                                               { "date" : {"order" : "desc"}},
                                                      
                                                       "size":5000,
                                                        "from":from_value
                                                        
                                                        })
        total=result_set['hits']['total']
        from_value=from_value + size
        with open(filename, 'a') as f:
            with  open('articles2.txt', 'a') as f1:
                for  hit in result_set['hits']['hits']:
                    i = i+1
                    print i, hit['origin'], hit['date']
                    c =  hit['_source']
                    f.write((c['article'] + c['keywords'] +c['focus']).encode('utf-8').replace('\n',' '))
                    f1.write((c['title'] + ". " +  c['keywords']).encode('utf-8').replace('\n',' '))
                    f.write("\n")
                    f1.write("\n")


create_lda_input_files()
