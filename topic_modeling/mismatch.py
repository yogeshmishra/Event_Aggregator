import sys
with open("corpus.txt","r") as corpus, open("topics.txt","r") as topics:
    line = 0
    while True:
        try:
            line +=1
            l1 , l2 = next(corpus), next(topics)
            print l1, l2
            l11 =  l1.split(',')
            l22 =  l2.split(',')
            l22 = filter(None, l22)
            print len(l11), len(l22)
            #l22 = filter("",l22)
            if len(l22)-1 != len(l11):
                print "LINE :", line
                print len(l11), len(l22)
                print l1, l2
                sys.exit()

        except:
            print "line ", line
            break

