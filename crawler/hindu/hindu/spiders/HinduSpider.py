import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from hindu.items import NewsItem

class HinduSpider(Spider):
        name = "hindu"
        #allowed_domains = ["thehindu.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
        start_urls =[]
        for year in range(2015,2016):
            for month in range(1,13):
                for day in range(1,32):
                    start_urls.append("http://www.thehindu.com/archive/web/"+ str(year) +"/"+ str(month).zfill(2) +"/"+ str(day).zfill(2) +"/")
        #start_urls = ["http://www.thehindu.com/archive/web/2016/01/01/"]
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
                for url in response.xpath('//div[@class="archiveWebListHolder"]//ul//li//a/@href').extract():
                        print url
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

                item["link"] = unicode(response.url)
                item["category"] = unicode(','.join(response.xpath('//h3[@class="cat"]/a/text()').extract()))
                item["title"] = unicode(response.xpath('//h1[@class="detail-title"]/text()').extract())
                item["author"] = unicode(','.join(response.xpath('//span[@class="artauthor"]//li/text()').extract()))
                item["date"] = unicode(''.join(response.xpath('//div[@class="artPubUpdate"]/text()').extract()).replace('Updated:','').replace("\n","").replace("\t","").replace("\r",""))
                item["focus"] = unicode(' '.join(response.xpath('//div[@class="articleLead"]//text()').extract()))
                item["article"] = unicode(' '.join(response.xpath('//div[@class="article-text"]//p[@class="body"]/text()').extract()).replace("\n","").replace("\t",""))
                item["origin"]="THE_HINDU"
                yield item
