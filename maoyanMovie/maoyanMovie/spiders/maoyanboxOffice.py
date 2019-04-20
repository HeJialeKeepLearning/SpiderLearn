# -*- coding: utf-8 -*-
import scrapy
import json
from maoyanMovie.items import boxofficeItem

class MaoyanboxofficeSpider(scrapy.Spider):
    name = 'maoyanboxOffice'
    allowed_domains = ['http://piaofang.maoyan.com/dashboard']
    start_urls = ['https://box.maoyan.com/promovie/api/box/second.json']

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
        "ITEM_PIPELINES": {'maoyanMovie.pipelines.boxOfficePipeline': 300}
    }

    def parse(self, response):
        jsonBody = json.loads(response.body.decode())
        subjects = jsonBody['data']['list']
        boxofficeItems = []
        for subject in subjects:
            item = boxofficeItem()
            item['avgSeatView'] = subject['avgSeatView']  # 上座率
            item['avgShowView'] = subject['avgShowView']  # 场均人次
            item['boxInfo'] = subject['boxInfo']  # 综合票房（万）
            item['boxRate'] = subject['boxRate']  # 票房占比
            item['movieId'] = str(subject['movieId'])  # 电影id
            item['movieName'] = subject['movieName']  # 电影名
            item['sumBoxInfo'] = subject['sumBoxInfo']  # 总票房
            item['showRate'] = subject['showRate']  # 排片占比

            boxofficeItems.append(item)
        return boxofficeItems
