import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ndtv.items import NewsItem
import dateutil.parser as dparser

def parseDate( date_string):
        return dparser.parse(date_string, fuzzy=True)



class NdtvSpider(Spider):
        name = "ndtv"
        #allowed_domains = ["thendtv.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
        start_urls =[]
        for year in range(2015,2017):
            for month in range(1,13):
                start_urls.append("http://archives.ndtv.com/articles/"+ str(year) +"-"+str(month)+".html")
        #start_urls = ["http://www.thendtv.com/archive/web/2016/01/01/"]
        baseURL1 = ""
        baseURL2 = ""
        def start_requests(self):
                for url in self.start_urls:
                    print "INDEX URL : " + url
                    yield scrapy.Request(url, self.parse, meta={
                        'splash': {
                            'endpoint': 'render.html',
                            'args': {'wait': 10.0}
                        }
                    })

        def parse(self, response):
                for url in response.xpath('//div[@id="main-content"]//ul//li//a/@href').extract():
                        #print url
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(url, callback = self.parseSave)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="article-text"]').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()
                if response.url.find("gadgets.ndtv.com") >= 0 : 
                    item["link"] = unicode(response.url)
                    item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                    item["category"] = unicode(''.join(response.xpath('//meta[@property="category"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["author"] = ""
                    date = parseDate(unicode(''.join(response.xpath('//meta[@property="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r","")))
                    item["date"] = date.strftime('%Y-%m-%d')
                    item["year"] = date.year
                    item["month"] = date.month
                    item["day"] = date.day
                    item["day_of_week"] = date.weekday()
                    item["focus"] = unicode(' '.join(response.xpath('//h1[@itemprop="headline"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["article"] = unicode(' '.join(response.xpath('//div[@itemprop="description"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["origin"] = "NDTV"
                    yield item
 
                elif response.url.find("profit.ndtv.com") >= 0 : 
                    item["link"] = unicode(response.url)
                    item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                    item["category"] = unicode(''.join(response.xpath('//meta[@property="category"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["author"] = unicode(' '.join(response.xpath('//div[@class="dateline"]/a/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    #item["date"] = unicode(''.join(response.xpath('//meta[@name="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    date = parseDate(unicode(''.join(response.xpath('//meta[@name="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r","")))
                    item["date"] = date.strftime('%Y-%m-%d')
                    item["year"] = date.year
                    item["month"] = date.month
                    item["day"] = date.day
                    item["day_of_week"] = date.weekday()
                    item["focus"] = unicode(' '.join(response.xpath('//p[@class="ins_mainimg_caption"]//text()').extract()))
                    item["article"] = unicode(' '.join(response.xpath('//div[@class="pdl200"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["origin"] = "NDTV"
                    yield item

                elif response.url.find("sports.ndtv.com") >= 0 : 
                    item["link"] = unicode(response.url)
                    item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                    item["category"] = unicode(''.join(response.xpath('//meta[@property="category"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["author"] = unicode(' '.join(response.xpath('//div[@class="dateline"]/a/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    #item["date"] = unicode(''.join(response.xpath('//meta[@name="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    date = parseDate(unicode(''.join(response.xpath('//meta[@name="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r","")))
                    item["date"] = date.strftime('%Y-%m-%d')
                    item["year"] = date.year
                    item["month"] = date.month
                    item["day"] = date.day
                    item["day_of_week"] = date.weekday()
                    item["focus"] = unicode(' '.join(response.xpath('//h2[@class="synopsis"]/text()').extract()))
                    item["article"] = unicode(' '.join(response.xpath('//div[@itemprop="articleBody"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["origin"] = "NDTV"
                    yield item

                elif response.url.find("www.ndtv.com") >= 0 : 
                    item["link"] = unicode(response.url)
                    item["keywords"] = unicode(''.join(response.xpath('//meta[@property="news_keywords"]/@content').extract()))
                    item["category"] = unicode(''.join(response.xpath('//meta[@property="section"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["title"] = unicode(''.join(response.xpath('//title/text()').extract()))
                    item["author"] = unicode(' '.join(response.xpath('//div[@class="ins_dateline"]//a/span/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    #item["date"] = unicode(''.join(response.xpath('//meta[@property="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    date = parseDate(unicode(''.join(response.xpath('//meta[@property="publish-date"]/@content').extract()).replace("\n","").replace("\t","").replace("\r","")))
                    item["date"] = date.strftime('%Y-%m-%d')
                    item["year"] = date.year
                    item["month"] = date.month
                    item["day"] = date.day
                    item["day_of_week"] = date.weekday()
                    item["focus"] = unicode(''.join(response.xpath('//meta[@property="description"]/@content').extract()))
                    item["article"] = unicode(' '.join(response.xpath('//div[@itemprop="articleBody"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                    item["origin"]="NDTV"
                    yield item
