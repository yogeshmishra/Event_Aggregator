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
    keywords =Field()
    category = Field()
    title = Field()
    author = Field()
    date = Field()
    year = Field()
    month = Field()
    day = Field()
    day_of_week = Field()
    article = Field()
    location = Field()
    focus=Field()
    origin = Field()
    pass
