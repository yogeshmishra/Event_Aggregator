import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from daily_excelsior.items import NewsItem

class daily_excelsiorSpider(Spider):
        name = "daily_excelsior"
        #allowed_domains = [""]
        start_urls = []
        for year in range(2015,2017):
            for month in range(1,13):
		for day in range(1,32):
                    start_urls.append("http://www.dailyexcelsior.com/" + str(year)+ "/" + str(month) + "/" + str(day)+ "/")
	baseURL1 = ""
        baseURL2 =  ""
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
	    totalurls = []
	    totalurls += response.xpath('//div[@id="dHost1"]//li/a/@href').extract()
	    totalurls += response.xpath('//div[@id="cHost1"]//li/a/@href').extract() 
 	    totalurls += response.xpath('//div[@class="state1"]//li/a/@href').extract()
	    totalurls += response.xpath('//div[@class="state2"]//li/a/@href').extract() 
	    totalurls += response.xpath('//div[@id="international"]//li/a/@href').extract()
	    totalurls += response.xpath('//div[@id="sports"]//li/a/@href').extract()
	    totalurls += response.xpath('//div[@id="national"]//li/a/@href').extract()
	    totalurls += response.xpath('//div[@id="business"]//li/a/@href').extract()
	    for url in totalurls: 
	    	yield scrapy.Request(self.baseURL1 + url, callback = self.parseSave)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="FL wd180 PL10"]/p/a/@href').extract() 
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()

                item["link"] = unicode(response.url)
                item["category"] = unicode(','.join(response.xpath('//meta[@property="article:section"]/@content').extract()))
                #item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                item["title"] = unicode(''.join(response.xpath('//meta[@property="og:title"]/@content').extract())) 
                item["date"] = unicode(''.join(response.xpath('//meta[@property="article:published_time"]/@content').extract())) 
                item["author"] = unicode(''.join(response.xpath('//span[@class="author vcard"]//text()').extract()))
                item["focus"] = unicode(''.join(response.xpath('//meta[@property="og:description"]/@content').extract()))
		loc = unicode("".join(response.xpath('//div[@class="entry-content"]/p/text()').extract())).split(',')
		item["location"] = loc[0] 
                item["article"] = unicode("".join(response.xpath('//div[@class="entry-content"]/p/text()').extract()).replace("\n","").replace("\t","").replace("\r","")) 
                item["origin"]="daily_excelsior"
                yield item
