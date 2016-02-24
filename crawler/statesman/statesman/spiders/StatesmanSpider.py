import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from statesman.items import NewsItem
import datetime
import dateutil.parser as dparser

def parseDate( date_string):
        return dparser.parse(date_string, fuzzy=True)



class StatesmanSpider(Spider):
        name = "statesman"
        #allowed_domains = ["thestatesman.com"]
        #start_urls = []
        #for x in xrange(1860,1865):
        #       start_urls.append("http://spiderbites.nytimes.com/free_" + str(x) + "/index.html"se_search_url="http://www.thestatesman.com/archive_search.aspx?txt=&catid="
        base_search_url="http://www.thestatesman.com/archive_search.aspx?txt=&catid="
        start_urls =[]
        cat_ids=[10,474,475,3,430,422,468,459,478,6,433,453,376,467,429,4,460,452,5,472,469,428,471,2]
        start_date_str = '10/01/2015'
        start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y")
        temp_date = start_date
        today = datetime.datetime.now()
        while temp_date < today:
            new_date= temp_date + datetime.timedelta(days=1)
            for cat_id in cat_ids:
                    start_urls.append(base_search_url + str(cat_id) + "&fd=" + temp_date.strftime('%m/%d/%Y %I:%M:%S %p') + "&td=" + new_date.strftime('%m/%d/%Y %I:%M:%S %p') )
            temp_date=new_date

        baseURL1 = "http://www.thestatesman.com"
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
                for url in response.xpath('//div[@class="secdiv"]/a/@href').extract():
                        baseURL1 = "http://www.thestatesman.com"
                        #print url
                        #self.log('@@@@ Got URL: %s' % (self.baseURL1+url))
                        #yield scrapy.Request(self.baseURL1 + url.split("_")[-3] + "/" + url, callback = self.parseNews) #There are two kinds format exist,e.g. 2003
                        yield scrapy.Request(baseURL1+url, callback = self.parseSave)


        def parseNews(self, response):
                News = []
                News_urls = response.xpath('//div[@class="article-text"]').extract()
                News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

                return News

        def parseSave(self, response):
                item = NewsItem()
                item["link"] = unicode(response.url)
                item["keywords"] = unicode(''.join(response.xpath('//meta[@name="keywords"]/@content').extract()))
                item["category"] = unicode(''.join(response.xpath('//div[@class="StoryCat"]/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["title"] = unicode(''.join(response.xpath('//title/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["author"] = unicode(' '.join(response.xpath('//div[@id="ctl00_ContentPlaceHolder2_Author"]//b/text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                date = parseDate(unicode(' '.join(response.xpath('//div[@id="ctl00_ContentPlaceHolder2_getdate"]//b/text()').extract()).replace("\n","").replace("\t","").replace("\r","")))
                #date =  parseDate(unicode(' '.join(response.xpath('//div[@class="story-timedate"]//text()').extract()).replace(u'\xa0',' ')))
                item["date"] = date.strftime('%Y-%m-%d')
                item["year"] = date.year
                item["month"] = date.month
                item["day"] = date.day
                item["day_of_week"] = date.weekday()
                item["focus"] = unicode(''.join(response.xpath('//meta[@property="description"]/@content').extract()))
                item["article"] = unicode(' '.join(response.xpath('//div[@id="contentStory"]//text()').extract()).replace("\n","").replace("\t","").replace("\r",""))
                item["origin"] = "STATESMAN"
                yield item

