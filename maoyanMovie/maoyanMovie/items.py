# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class top100Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 电影名
    stars = scrapy.Field()  # 主演
    releaseTime = scrapy.Field()  # 上映时间
    poster = scrapy.Field()  # 海报
    rate = scrapy.Field()  # 评分

class movieItem(scrapy.Item):
    name = scrapy.Field()  # 电影名
    stars = scrapy.Field()  # 演员信息
    releaseTime = scrapy.Field()  # 上映时间
    poster = scrapy.Field()  # 海报
    rate = scrapy.Field()  # 评分
    id = scrapy.Field()  # 电影id
    reviewNum = scrapy.Field()  # 评论人数
    boxOffice = scrapy.Field()  # 电影票房
