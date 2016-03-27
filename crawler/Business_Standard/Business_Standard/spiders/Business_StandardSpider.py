import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from Business_Standard.items import NewsItem

class Business_StandardSpider(Spider):
        name = "Business_Standard"
        #allowed_domains = [""]
        start_urls = []
        for year in range(2015,2017):
            for month in range(1,13):
		for day in range(1,32):
		    for page in range(1,10):  
                	start_urls.append("http://www.business-standard.com/advance-search?advance=Y&type=print-media&print_date=" + str(day) +"-" + str(month) +"-"+ str(year) + "&itemsPerPage=19&page=" + str(page))
        baseURL1 = "http://www.business-standard.com"
        baseURL2 =  "http://www.business-standard.com"
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
	    for url in response.xpath('//ul[@class="listing"]//h2/a/@href').extract(): 
	    	yield scrapy.Request(self.baseURL1 + url, callback = self.parseSave)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="FL wd180 PL10"]/p/a/@href').extract() 
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()

                item["link"] = unicode(response.url)
                item["category"] = unicode(','.join(response.xpath('//div[@class="breadcrum"]//text()').extract()[3:]).replace(u' \xbb ,','')) 
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                item["title"] = unicode(''.join(response.xpath('//h1[@class="headline"]/text()').extract())) 
                item["date"] = unicode(''.join(response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0:1])) 
                item["author"] = unicode(''.join(response.xpath('//meta[@name="author"]/@content').extract())) 
                item["focus"] = unicode(''.join(response.xpath('//h2[@itemprop="alternativeHeadline"]/text()').extract()))
		item["location"] = unicode(''.join(response.xpath('//geo_locations/text()').extract()))
                item["article"] = unicode(''.join(response.xpath('//p[@itemscope= "articleBody"]/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["origin"]="Business_Standard"
                yield item
