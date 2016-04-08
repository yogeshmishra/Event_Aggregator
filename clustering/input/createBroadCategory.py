import sys
import ast

def createTopicToCategoryMap():
    
    TopicToCategoryMap = []
    i = 0
    with open("topicNames.txt", 'r+') as topics, open("MapTopicstocategory.txt", 'r+') as category:
        categorylist = []
        topicList = []
        for line2 in category:
            categorylist.append(line2.replace('\n','').strip().encode('utf-8'))
        
        for line in topics:
            topicList.append(unicode(line.replace('\n','').strip()))
            
        TopicToCategoryMap = zip(topicList, categorylist)

    TopicToCategoryMap = dict(TopicToCategoryMap)
    return TopicToCategoryMap


def createBroadCategory(TopicToCategoryMap):
    
    with open("categories.txt", 'r+') as categories, open("broadCategory.txt", 'w') as broadCat:
        for line in categories:
            category_dict = ast.literal_eval(line)
            category_dict = sorted([(value,key) for (key,value) in category_dict.items()], cmp=None, key=None, reverse=True)
            print category_dict
            for key in category_dict:
                if(TopicToCategoryMap[key[1]] != ''):
                    broadCat.write(TopicToCategoryMap[key[1]])
                    break
            broadCat.write('\n')
            


if __name__=="__main__":
    categoryMap = createTopicToCategoryMap()
    print categoryMap

    createBroadCategory(categoryMap)

