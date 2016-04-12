import sys
import ast
import hashlib
import networkx
from pprint import pprint
def pairs(lst):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first

def createArticleList():
    article_list =[]
    
    with open('../data/titles.txt','r') as titles, open('../data/links.txt','r') as links, open('../data/ids.txt','r') as ids, open('../data/enriched_keys.txt','r') as enriched_keys, open('../data/locations.txt','r') as locs:
        while True:
            try:
                article = {}
                id , link, enriched_key, title, location = next(ids).strip() ,next(links).strip(), ast.literal_eval(next(enriched_keys)), next(titles).strip(),ast.literal_eval(next(locs))
                article['id'] = id
                article['link'] = link
                article['title'] = title
                article['enriched_keys'] = enriched_key
                article['location'] = location
                article_list.append(article)
            except Exception as e:
                print "READ ERROR : LINE ", str(e)
                break
    return article_list

def createArticleSet():
    lists = []
    threshold = 1.5
    with open('output.txt','r') as events:
        for line in events:
            line = ast.literal_eval(line)
            temp_list = []
            for elem in line:
                if(elem[1] > threshold):
                    temp_list.append(elem[0])
                else:
                    break
            lists.append(temp_list)
    return lists

if __name__=="__main__":

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])

    date= str(year)+"-"+str(month) + "-" + str(day)
    lists = createArticleSet()
    g = networkx.Graph()
    for sub_list in lists:
        for edge in pairs(sub_list):
                g.add_edge(*edge)

    event_set = networkx.connected_components(g)
    for s in event_set:
        print s
"""        
    article_list = createArticleList()
    events_list =[]
    for sets in event_set:
        event = {}
        event['articles']= []
        event['id'] = ''
        event['enriched_keys'] = []
        event['location'] = []
        for elem in sets:
            event['title'] = article_list[elem]['title']
            event['id'] = event['id'] + article_list[elem]['id']
            event['articles'].append(article_list[elem])
            event['location'] = event['location'] + article_list[elem]['location']
            event['enriched_keys'] = event['enriched_keys'] + article_list[elem]['enriched_keys']
        
        event['location'] = set(event['location'])
        event['enriched_keys'] = set(event['enriched_keys'])
        event['date'] = date
        event['year'] = year
        event['month'] = month
        event['day'] = day
        hash_object = hashlib.md5(event['id'])
        event['id'] = hash_object.hexdigest()


        pprint(event)
        events_list.append(event)

    print(events_list[0])
"""
