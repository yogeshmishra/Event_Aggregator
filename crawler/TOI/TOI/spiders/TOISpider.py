import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from TOI.items import NewsItem

class NYtimesSpider(Spider):
        name = "TOI"
        allowed_domains = [""]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
        start_urls = ["http://spiderbites.nytimes.com/free_2014/index.html"]
        baseURL1 = "http://spiderbites.nytimes.com"
        baseURL2 = "http://www.nytimes.com/"

        def parse(self, response):
                for url in response.xpath('//div[@class="articlesMonth"]/ul/li/a/@href').extract():
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(self.baseURL1 + url, callback = self.parseNews)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//span[@style="font-family:arial ;font-size:12;color: #006699"]/a/@href').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()

                item["link"] = unicode(response.url)
                item["category"] = unicode(','.join(response.xpath('//div[@class="navbdcrumb"]//text()').extract()[2:]))
                item["title"] = unicode(response.xpath('//h1[@class="heading1"]/text()').extract())
                dateItem = unicode(response.xpath('//span[@class="time_c    ptn"]/text()').extract())
                dateItem = dateItem.split("|")
                item["author"] = ""
                if(len(dateItem) > 2)
                    item["author"] = dateItem[0]
                item["date"] = dateItem[len(dateItem) - 1]
                item["article"] = unicode(response.xpath('//div[@class="Normal"]//text()').extract())
                item["origin"]="TOI"
                yield item
