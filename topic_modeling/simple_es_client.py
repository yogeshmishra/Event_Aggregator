import json
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'}])
basefolder = 'rawFiles/'
def create_lda_input_files(size=5000, filename="articles.txt", month =12 , year = 2015):
    print "Parameters are: " +  "Size: " + str(size) + " filename = " + filename + " month : " + str(month) + " year : " + str(year)
    from_value=0
    total=1
    i=0 
    os.remove(filename)
    os.remove(basefolder +'articles2.txt')
    os.remove(basefolder + 'id.txt')
    while total > from_value:
        result_set = es.search(index="jan_news",body={
        "query": {
           "bool": {
                "must": [
                       { "match": { "month": month } },
                       {"match": {"year":year}}
                              
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
                with open(basefolder +'id.txt', 'a') as f2:        
                    for  hit in result_set['hits']['hits']:
                        i = i+1
                        if i%500  == 0 :
                            print i
                        c =  hit['_source']
                        #print hit['_id'],c
                        appended_words = c['title'] + ". " +  c.get('keywords'," ") + ". "+ c['focus']
                        if len(appended_words.split(" ")) > 4:
                            f1.write((c['article'] + c.get('keywords',"") +c['focus']).encode('utf-8').replace('\n',' '))
                            f.write((c['title'] + ". " +  c.get('keywords',"") + ". "+ c['focus']).encode('utf-8').replace('\n',' '))
                            f2.write(hit['_id'].encode('utf-8'))
                            f.write("\n")
                            f1.write("\n")
                            f2.write("\n")

if __name__=="__main__":
    s = 500
    f="articles.txt"
    month = 12
    year = 2015
    i = 1
    while i < len(sys.argv) :
        if(i == 1):
            s = int(sys.argv[1])
        elif i == 2 :
            f= sys.argv[2]
        elif i == 3  :
            month = int(sys.argv[3])
        elif i == 4 :
            year = int(sys.argv[4])
        i = i+1 

    create_lda_input_files(size=s,filename=basefolder+f, month=month, year=year)
