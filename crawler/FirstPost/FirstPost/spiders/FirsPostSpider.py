import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from FirstPost.items import NewsItem

import dateutil.parser as dparser

def parseDate( date_string):
    return dparser.parse(date_string, fuzzy=True)

class FirstPostSpider(Spider):
        name = "FirstPost"
        #allowed_domains = [""]
        start_urls = []
	categorylist = [1, 3,4,5,6,7,9,399,36]
        for year in range(2015,2017):
            for month in range(1,13):
		for day in range(1,32):
		    for category in categorylist:  
                	start_urls.append("http://www.firstpost.com/archive/?year=" + str(year) +"&month=" + str(month) +"&day="+ str(day) + "&cat=" + str(category))
        baseURL1 = "http://www.firstpost.com"
        baseURL2 =  "http://www.firstpost.com" 
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
	    total_pages =[]
	    total_pages.append(response.url)
	    extra_pages = response.xpath('//ul[@class="pagination"]//a/@href').extract()
	    if(len(extra_pages) > 0):
	        total_pages += extra_pages[1:len(extra_pages)-1]
	    for url in total_pages:
                print url
		if(url[0] == 'h'):
		    yield scrapy.Request(url, callback = self.parseNews)
                else:
		    yield scrapy.Request(self.baseURL1 + url, callback = self.parseNews)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="FL wd180 PL10"]/p/a/@href').extract() 
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()

                item["link"] = unicode(response.url)
                item["category"] = unicode(','.join(response.xpath('//span[@itemprop="title"]/text()').extract()[1:]))
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                item["title"] = unicode(''.join(response.xpath('//h1[@class="artTitle"]/text()').extract()))
                date = parseDate(unicode(''.join(response.xpath('//meta[@property="article:published_time"]/@content').extract())))
                item["date"] = date.strftime('%Y-%m-%d')
                item["year"] = date.year
                item["month"] = date.month
                item["day"] = date.day
                item["day_of_week"] = date.weekday()
                item["author"] = unicode(''.join(response.xpath('//span[@class="by"]/a/text()').extract())) 
                item["focus"] = unicode(''.join(response.xpath('//meta[@name="description"]/@content').extract()))
                item["article"] = unicode(' '.join(response.xpath('//div[@class="fullCont1"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["origin"]="FIRST_POST"
                yield item
