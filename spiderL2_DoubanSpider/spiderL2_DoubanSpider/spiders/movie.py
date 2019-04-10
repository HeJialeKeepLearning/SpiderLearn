# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from spiderL2_DoubanSpider.items import movieItem


class MovieSpider(scrapy.Spider):

    name = 'movie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json, text/javascript,*/*;q=0.01',
            'accept - encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': ' https://movie.douban.com/tag/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        },
        "ROBOTSTXT_OBEY": False,
        "ITEM_PIPELINES": {'spiderL2_DoubanSpider.pipelines.moviePipeline': 300}
    }

    def start_requests(self):
        url = '''https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={start}'''
        requests = []
        for i in range(2):
            request = Request(url.format(start = i * 20), callback = self.parse_movie)
            requests.append(request)
        return requests

    def parse_movie(self, response):

        jsonBody = json.loads(response.body.decode())
        subjects = jsonBody['data']
        movieItems = []
        for subject in subjects:
            item = movieItem()
            item['id'] = int(subject['id'])
            item['title'] = subject['title']
            item['rating'] = float(subject['rate'])
            item['alt'] = subject['url']
            item['image'] = subject['cover']
            movieItems.append(item)
        return movieItems
