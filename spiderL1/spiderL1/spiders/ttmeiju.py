# -*- coding: utf-8 -*-
import scrapy
from spiderL1.items import Spiderl1Item


class TtmeijuSpider(scrapy.Spider):
    name = 'ttmeiju'#让scrapy框架定位爬虫的名称，必须唯一
    allowed_domains = ['meijutt.com']
    start_urls = ['https://www.meijutt.com/new100.html']

    def parse(self, response):
        movies=response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for movie in movies:
            item=Spiderl1Item()
            item['name']=movie.xpath('./h5/a/@title').extract()[0]
            yield item