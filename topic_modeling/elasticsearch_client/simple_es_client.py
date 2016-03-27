from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{'host':'db03.cs.utah.edu'},{'host':'db04.cs.utah.edu'}])

result_set = es.search(index="news",body={"query":{"bool":{"must":[{"match":{"month":"2"}},{"match":{"origin":"NDTV"}}]}},"sort":{"date":{"order":"desc"}},"size":50,"from":99})

for  hit in result_set['hits']['hits']:
    print hit['_source']
    print "#################################################"
