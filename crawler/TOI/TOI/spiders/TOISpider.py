import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from TOI.items import NewsItem

class NYtimesSpider(Spider):
        name = "TOI"
        #allowed_domains = [""]
        start_urls = []
        for year in range(2015,2017):
            for month in range(1,13):
                start_urls.append("http://timesofindia.indiatimes.com/archive/year-" + str(year) +",month-" + str(month) +".cms")
        baseURL1 = "http://timesofindia.indiatimes.com"
        baseURL2 = "http://timesofindia.indiatimes.com"

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
            for url in response.xpath('//td[@align="center"]/a/@href').extract():
                print url
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
                dateItem = unicode(response.xpath('//span[@class="time_cptn"]/text()').extract())
                dateItem = dateItem.split("|")
                item["author"] = ""
                if(len(dateItem) > 2):
                    item["author"] = dateItem[0]
                item["date"] = dateItem[len(dateItem) - 1]
                item["focus"] = ""
                item["article"] = unicode(' ', join(response.xpath('//div[@class="Normal"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["origin"]="TOI"
                yield item
