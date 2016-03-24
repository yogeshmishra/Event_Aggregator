import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from hindu.items import NewsItem
import dateutil.parser as dparser

def parseDate( date_string):
        return dparser.parse(date_string, fuzzy=True)

class HinduSpider(Spider):
        name = "hindu"
        #allowed_domains = ["thehindu.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html")
        start_urls =[]
        for year in range(2015,2017):
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
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                item["category"] = unicode(','.join(response.xpath('//meta[@property="article:section"]/@content').extract()))
                item["title"] = unicode(' '.join(response.xpath('//meta[@property="og:title"]/@content').extract()))
                item["author"] = unicode(','.join(response.xpath('//meta[@name="author"]/@content').extract()))
                date = parseDate(unicode(' '.join(response.xpath('//meta[@property="article:published_time"]/@content').extract())))
                item["date"] = date.strftime('%Y-%m-%d')
                item["year"] = date.year
                item["month"] = date.month
                item["day"] = date.day
                item["day_of_week"] = date.weekday()
                item["focus"] = unicode(' '.join(response.xpath('//meta[@name="description"]/@content').extract())).replace("\n","").replace("\t","")
                item["article"] = unicode(' '.join(response.xpath('//div[@class="article-text"]//p[@class="body"]/text()').extract()).replace("\n","").replace("\t","").replace(u'\xa0',' '))
                item["origin"]="THE_HINDU"
                yield item
