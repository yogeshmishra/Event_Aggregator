# -*- coding: utf-8 -*-

# Scrapy settings for NYtimes project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from scrapy import log

BOT_NAME = 'NYtimes'

SPIDER_MODULES = ['NYtimes.spiders']
NEWSPIDER_MODULE = 'NYtimes.spiders'
ITEM_PIPELINES = {
	'NYtimes.pipelines.NYtimesPipeline' : 500,
}
ITEM_PIPELINES = [
            'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline',
            ]

ELASTICSEARCH_SERVER = 'localhost' # If not 'localhost' prepend 'http://'
ELASTICSEARCH_PORT = 9200 # If port 80 leave blank
ELASTICSEARCH_USERNAME = ''
ELASTICSEARCH_PASSWORD = ''
ELASTICSEARCH_INDEX = 'news'
ELASTICSEARCH_TYPE = 'articles'
ELASTICSEARCH_UNIQ_KEY = 'url'  # Custom uniqe key like 'student_id'
ELASTICSEARCH_LOG_LEVEL= log.DEBUG
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'NYtimes (+http://www.yourdomain.com)'
