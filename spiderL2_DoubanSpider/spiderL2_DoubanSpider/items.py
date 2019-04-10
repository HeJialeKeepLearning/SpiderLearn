# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spiderl2DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class movieItem(scrapy.Item):
    id =scrapy.Field()
    title=scrapy.Field()
    rating = scrapy.Field()
    original_title = scrapy.Field()
    genres = scrapy.Field()
    alt = scrapy.Field()
    image = scrapy.Field()
    year = scrapy.Field()
