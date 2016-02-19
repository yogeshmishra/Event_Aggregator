# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy.item import Item, Field


class NewsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    link = Field()
    category = Field()
    title = Field()
    author = Field()
    date = Field()
    article = Field()
    location = Field()
    origin = Field()
    pass
