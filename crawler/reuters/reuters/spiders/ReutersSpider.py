import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from reuters.items import NewsItem

class ReutersSpider(Spider):
        name = "reuters"
        allowed_domains = ["reuters.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
        start_urls = ["http://www.reuters.com/resources/archive/us/2015.html"]
        baseURL1 = "http://www.reuters.com"
        baseURL2 = "http://www.reuters.com"

        def parse(self, response):
                for url in response.xpath('//div[@class="moduleBody"]/p/a/@href').extract():
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(self.baseURL1 + url, callback = self.parseNews)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="headlineMed"]/a/@href').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()

                item["link"] = unicode(response.url)
                try:
                        item["category"] = unicode(response.xpath('//span[@class="article-section"]/text()').extract()[0])
                except:
                        item["category"] = ""
                        pass
                try:        
                        item["title"] = unicode(response.xpath('//h1[@class="article-headline"]/text()').extract()[0])
                except:
                        item["title"] = ""
                try:
                        item["author"] = unicode(response.xpath('//span[@class="byline"]/a/text()').extract()[0])
                except:
                        item["author"] = ""
                        pass
                try:
                        item["date"] = unicode(response.xpath('//span[@class="timestamp"]/text()').extract()[0])
                except:
                        item["date"] = ""
                        pass
                #item["article"] = response.xpath('//span[@class="focusParagraph"]/p/text()').extract()[0]
                try:
                        item["article"] = response.xpath('//span[@id="articleText"]/p/text()').extract()
                except:
                        item["article"] = ""
                        pass
                item["origin"] = "REUTERS"
                yield item
