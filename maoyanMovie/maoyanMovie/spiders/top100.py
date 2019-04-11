# -*- coding: utf-8 -*-
import scrapy
from maoyanMovie.items import top100Item

class Top100Spider(scrapy.Spider):
    name = 'top100'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4/']

    custom_settings = {
        "ITEM_PIPELINES": {'maoyanMovie.pipelines.top100Pipeline': 300}
    }

    # def start_requests(self):
    #     url = '''https://maoyan.com/board/4?offset={offset}'''
    #     requests = []
    #     for i in range(10):
    #         request = scrapy.Request(url.format(offset = 10 * i), callback = self.parse)
    #         requests.append(request)
    #     return requests

    def parse(self, response):
        movies = response.xpath('//dl[@class="board-wrapper"]/dd')
        for movie in movies:
            item = top100Item()
            # 电影名
            item['name'] = movie.xpath('./a[@class="image-link"]/@title').extract()[0]
            # 主演
            item['stars'] = movie.xpath('.//p[@class="star"]/text()').extract()[0].strip()
            # 上映时间
            item['releaseTime'] = movie.xpath('.//p[@class="releasetime"]/text()').extract()[0].strip()
            # 海报,用data-src而非src提取
            item['poster'] = movie.xpath('.//img[@class="board-img"]/@data-src').extract()[0]
            # 评分
            item['rate'] = ''.join(movie.xpath('.//p[@class="score"]/i/text()').extract()).strip()

            # yield item
            print(item['name'])
