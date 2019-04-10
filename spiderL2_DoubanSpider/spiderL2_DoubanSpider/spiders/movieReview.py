# -*- coding: utf-8 -*-
import scrapy


class MoviereviewSpider(scrapy.Spider):
    name = 'movieReview'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def parse(self, response):
        pass
