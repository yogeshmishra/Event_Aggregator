import json
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])
basefolder = 'input/'
def create_input_files(size=5000, month =12 , year = 2015, day = 02, section = "Finance"):
    print "Parameters are: " +  "Size: " + str(size) + " day = " + str(day) + " month : " + str(month) + " year : " + str(year)
    print "Section:", section
    from_value=0
    total=1
    i=0
    try:
        os.remove(basefolder + 'ids.txt')
        os.remove(basefolder+"corpus.txt")
        os.remove(basefolder +'enriched_keys.txt')
        os.remove(basefolder +'titles.txt')
        os.remove(basefolder +'links.txt')
    except:
        pass
    while total > from_value:
        result_set = es.search(index="jan_news", body={
            "query": {
                        "filtered": {
                            "query":{
                                "match":{
                                    "section":section
                                }
                            },
                            "filter": {
                                "range": {"date": {"gte": str(year) + "-" + str(month) + "-" + str(day) + "||-1d/d",
                                           "lte": str(year) + "-" + str(month) + "-" + str(day) + "||+1d/d",
                                           "format": "yyyy-MM-dd||dd"}}
                            }
                        }   
                    },  
                    "sort": {
                        "date": {
                            "order": "asc"
                        },  
                        "link": {"order": "asc"}
                    },  
                    "size": size,
                    "from": from_value
                })

        total = result_set['hits']['total']
        from_value=from_value + size
        with open(basefolder+"corpus.txt", 'a+') as corpus, open(basefolder+'enriched_keys.txt', 'a+') as keys, open(basefolder +'ids.txt', 'a+') as ids, open(basefolder +'titles.txt', 'a+') as titles, open(basefolder +'links.txt', 'a+') as links  :
                    for  hit in result_set['hits']['hits']:
                        i = i+1
                        if i%500  == 0 :
                            print i
                        c =  hit['_source']
                        appended_words = c['title'] + c['article'] + c.get('keywords','') + c['focus']
                        if len(appended_words.split(" ")) > 4:
                            print hit['_id'] , c['section']
                            corpus.write((c['title'] + c['article'] + c.get('keywords','') + c['focus']).encode('utf-8').replace('\n',' '))
                            keywords = (c.get('enriched_keywords',"") ).encode('utf-8').replace('\n',' ')
                            keywords = keywords.split(',')
                            keys.write(unicode(keywords))
                            ids.write(hit['_id'].encode('utf-8'))
                            titles.write((c.get('title',"") ).encode('utf-8').replace('\n',' '))
                            links.write((c.get('link',"") ).encode('utf-8').replace('\n',' '))
                            corpus.write("\n")
                            keys.write("\n")
                            ids.write("\n")
                            titles.write("\n")
                            links.write("\n")

if __name__=="__main__":
    s = 500
    month = 12
    year = 2015
    section= "Finance"
    i = 1
    while i < len(sys.argv) :
        if(i == 1):
            s = int(sys.argv[1])
        elif i == 2  :
            year = int(sys.argv[2])
        elif i == 3 :
            month = int(sys.argv[3])
        elif i == 4 :
            day = int(sys.argv[4])
        elif i == 5 :
            section = sys.argv[5]
        i = i+1 

    create_input_files(size=s, month=month, year=year, section=section)
