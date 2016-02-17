import scrapy
from NYtimes.items import NYtimesItem

class NYtimesSpider(scrapy.Spider):
	name = "WSJ"
	allowed_domains = ["wsj.com"]
	#start_urls = []
	#for x in xrange(1860,1865):
	#	start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
	start_urls = ["http://www.wsj.com/public/page/archive-2015-1-1.html"]
	baseURL1 = "http://www.wsj.com"
	baseURL2 = "http://www.wsj.com"

	def parse(self, response):
		for url in response.xpath('//div[@class="moduleBody"]/p/a/@href').extract():
			#self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
			#yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
			yield scrapy.Request(self.baseURL1 + url, callback = self.parseNews)


	def parseNews(self, response):
		News = []
		News_urls =  response.xpath('//td/a/@href').extract() 
		News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

		return News

	def parseSave(self, response):
		item = NYtimesItem()

		item["link"] = unicode(response.url)
		try:
			item["category"] = unicode(response.xpath('//span[@class="article-section"]/text()').extract()[0])
		except:
			item["category"] = ""
			pass
			
		item["title"] = unicode(response.xpath('//h1[@class="article-headline"]/text()').extract()[0])
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
		item["article"] = response.xpath('//span[@class="focusParagraph"]/p/text()').extract()[0]
		try:
			item["article"] = response.xpath('//span[@id="articleText"]/p/text()').extract()
		except:
			item["article"] = ""
			pass
		yield item
