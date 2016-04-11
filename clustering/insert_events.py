import json
from collections import Counter
import math
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'}])

   
def upsert_event(Client, event):
    """
        structure of event        
        {
          "id": "e17f6d76897496f2911726401e9efecd72d2da57",
          "title":"Title comes here",
          "articles":[
              {
               "id": "id1",
               "link": "http://economictimes.com/adjaccaasd",
               "title": "articles title"
              },
              {
               "id": "id2",
               "link": "http://economictimes.com/adjdaasdqa",
               "title": "articles title"
              }
            ],
            "date":"2016-01-01",
            "year":2016,
            "month" : 1,
            "day": 1,
            "keywords": "key1,key2,key3",
            "location": "loc1,loc2,loc3",
            "category": "category name"
        }

    """
    id = event['id']
    Client.update(index="testevents", doc_type="news", id=id, body={"doc":event,'doc_as_upsert':True})

if __name__=="__main__":
    event={}
    event['id']= "1"
    upsert_event(es, event)
