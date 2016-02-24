import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from betterindia.items import NewsItem
import datetime
import dateutil.parser as dparser

def parseDate( date_string):
        return dparser.parse(date_string, fuzzy=True)


class BetterindiaSpider(Spider):
        name = "betterindia"
        #allowed_domains = ["thebetterindia.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html"se_search_url="http://www.thebetterindia.com/archive_search.aspx?txt=&catid="
        base_search_url="http://www.thebetterindia.com/date/"
        start_urls=[]
        for year in range(2015,2016):
            for month in range(1,13):
                    start_urls.append(base_search_url + str(year) + "/" + str(month) + "/" )

        baseURL1 = "http://www.thebetterindia.com"
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
                urls = response.xpath('//nav[@class="page-navigation"]//a/@href').extract()
                urls.append(response.url)
                for url in set(urls):
                        #print url
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(url, callback = self.parseNews)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@id="main"]//h2[@class="h4"]//a/@href').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()
                item["link"] = unicode(response.url)
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="keywords"]/@content').extract()))
                item["category"] = unicode(''.join(response.xpath('//meta[@property="article:section"]/@content').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["author"] = unicode(' '.join(response.xpath('//div[@class="cb-author"]//a/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                date = parseDate(unicode(' '.join(response.xpath('//meta[@property="article:published_time"]/@content').extract()).replace("\n","").replace("\t","").replace("\r","")))
                item["date"] = date.strftime('%Y-%m-%d')
                item["year"] = date.year
                item["month"] = date.month
                item["day"] = date.day
                item["day_of_week"] = date.weekday()
                item["focus"] = unicode(''.join(response.xpath('//meta[@name="description"]/@content').extract()))
                item["article"] = unicode(' '.join(response.xpath('//section[@itemprop="articleBody"]//p/text() | //section[@itemprop="articleBody"]//h2/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["origin"] = "BETTER_INDIA"
                yield item

