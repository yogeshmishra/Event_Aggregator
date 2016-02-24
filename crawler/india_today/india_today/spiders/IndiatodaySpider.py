import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from india_today.items import NewsItem
import datetime
import dateutil.parser as dparser

def parseDate( date_string):
    return dparser.parse(date_string, fuzzy=True)

class IndiatodaySpider(Spider):
        name = "india_today"
        #allowed_domains = ["theindia_today.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html"se_search_url="http://www.theindia_today.com/archive_search.aspx?txt=&catid="
        base_search_url="http://indiatoday.intoday.in/calendar/"
        start_urls=[]
        start_date_str = '10/01/2015'
        start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y")
        temp_date = start_date
        today = datetime.datetime.now()
        while temp_date < today:
            start_urls.append(base_search_url  + temp_date.strftime('%d-%m-%Y') + "/online.html"  )
            temp_date= temp_date + datetime.timedelta(days=1)


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
                urls = response.xpath('//div[@class="secheadtext"]//a/@href').extract()
                for url in set(urls):
                        #print url
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(url, callback = self.parseSave)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@id="main"]//h2[@class="h4"]//a/@href').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

            
        def parseSave(self, response):
                item = NewsItem()
                item["link"] = unicode(response.url)
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="news_keywords"]/@content').extract()))
                item["category"] = unicode(' '.join(response.xpath('//div[@class="path"]//span/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["author"] = unicode(' '.join(response.xpath('//div[@class="authername"]//a/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                date =  parseDate(unicode(' '.join(response.xpath('//div[@class="story-timedate"]//text()').extract()).replace(u'\xa0',' ')))
                item["date"] = date.strftime('%Y-%m-%d')
                item["year"] = date.year 
                item["month"] = date.month
                item["day"] = date.day
                item["day_of_week"] = date.weekday()
                item["focus"] = unicode(''.join(response.xpath('//meta[@name="description"]/@content').extract()))
                item["article"] = unicode(' '.join(response.xpath('//div[@class="right-story-container"]//text()').extract()).replace("\n","").replace(u'\xa0',"").replace("\r",""))
                item["origin"] = "INDIA_TODAY"
                yield item

