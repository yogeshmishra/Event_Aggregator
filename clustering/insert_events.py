import json
from collections import Counter
import math
import sys, os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'}])

   
def upsert_event(Client, event):
    id = event['id']
    Client.update(index="testevents", doc_type="news", id=id, body={"doc":event,'doc_as_upsert':True})

if __name__=="__main__":
    event={}
    event['id']= "1"
    upsert_event(es, event)
