# -*- coding: utf-8 -*-
import scrapy
from maoyanMovie.items import movieItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    custom_settings = {
        "ITEM_PIPELINES": {'maoyanMovie.pipelines.moviePipeline': 300},
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://maoyan.com/films?showType=3&offset=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        },
        "ROBOTSTXT_OBEY": False
    }

    def start_requests(self):
        url = '''https://maoyan.com/films?showType=3&offset={offset}'''
        requests = []
        for i in range(100):
            request = scrapy.Request(url.format(offset = 30 * i), callback = self.parse)
            requests.append(request)
        return requests

    def parse(self, response):
        movies = response.xpath('//dl[@class="movie-list"]/dd')

        movieItemNames = movies.xpath('.//div[@class="channel-detail movie-item-title"]/@title').extract()
        movieItemPosters = movies.xpath('.//div[@class="movie-poster"]/img/@data-src').extract()
        movieItemIds = movies.xpath('.//a[@data-act="movie-click"]/@data-val').extract()
        movieItemIndex = 0

        while movieItemIndex < len(movieItemNames):
            item = movieItem()
            # 电影名
            item['name'] = movieItemNames[movieItemIndex]
            # 海报url,用data-src而非src提取,后面16个字符是控制缩略图的，省略掉则可以访问原图
            item['poster'] = movieItemPosters[movieItemIndex][:-16]
            # 电影id,去掉自带的movieId等信息，只需要数字即可
            item['id'] = movieItemIds[movieItemIndex][9:-1]

            movieItemIndex += 1
            yield item
