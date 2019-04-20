# -*- coding: utf-8 -*-
import scrapy
import pymysql
from maoyanMovie.items import movieItem
import re
from fontTools.ttLib import TTFont
import os
import requests

# 为下载字体库创建文件夹
os.makedirs('fonts', exist_ok = True)
# 构造request用前缀
pre = 'https://maoyan.com/films/'
# 正则匹配
regex_woff = re.compile("(?<=url\(').*\.woff(?='\))")
regex_text = re.compile('(?<=<span class="stonefont">).*?(?=</span>)')
regex_font = re.compile('(?<=&#x).{4}(?=;)')
# 手工确认好的对应表
basefont = TTFont('base.woff')
fontdict = {'uniF32E': '2', 'uniE824': '7', 'uniF092': '9', 'uniF6FB': '4', 'uniEBD6': '8',
            'uniF270': '0', 'uniF451': '6', 'uniEF3D': '3', 'uniE284': '1', 'uniEFBD': '5'}

# 全局的处理函数
def get_fontnumber(newfont, text):
    ms = regex_font.findall(text)
    for m in ms:
        text = text.replace(f'&#x{m};', get_num(newfont, f'uni{m.upper()}'))
    return text

def get_num(newfont, name):
    uni = newfont['glyf'][name]
    for k, v in fontdict.items():
        if uni == basefont['glyf'][k]:
            return v

def downloads(url, localfn):
    with open(localfn, 'wb+') as sw:
        sw.write(requests.get(url).content)

class MovieinfoSpider(scrapy.Spider):
    name = 'movieInfo'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    custom_settings = {
        "ITEM_PIPELINES": {'maoyanMovie.pipelines.movieInfoPipeline': 300},
        "DEFAULT_REQUEST_HEADERS": {
            'connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': 1,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://maoyan.com/films?showType=3&offset=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        },
        "ROBOTSTXT_OBEY": False,
        "RETRY_TIMES": 9,
        "DOWNLOAD_TIMEOUT": 3,
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):
        # 从数据库中找到所有的moviesId
        # 连接数据库
        config = {
            'host': 'host',
            'port': 3306,
            'user': 'username',  # 连接数据库的用户
            'password': 'password',
            'database': 'databasename',  # 数据库名
            'charset': 'utf8',
            'use_unicode': True,
            'autocommit': True,
        }
        self.connect = pymysql.connect(**config)
        self.cursor = self.connect.cursor()

        sql = "select id from maoyanMovie"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        url_fromsql = []

        for ri in results:
            url_fromsql.append(list(ri))

        url_format = '''https://maoyan.com/films/{id}'''

        for i in url_fromsql:
            id = i[0]
            url = url_format.format(id = id)
            request = scrapy.Request(url = url, callback = self.parse, meta = {'id': id}, dont_filter = True)
            yield request

    def parse(self, response):
        item = movieItem()
        item['id'] = response.request.meta['id']
        # 演员信息列表
        starlist = response.xpath('//div[@class="celebrity-group"]/div[@class="celebrity-type"]')[1].xpath(
            '//following-sibling::li[@class="celebrity actor"]/div[@class="info"]/a[@class="name"]/text()').extract()[
                   0:4]
        itemstars = ''
        for star in starlist:
            itemstars = itemstars + star.strip() + ','
        item['stars'] = itemstars
        # 上映时间
        item['releaseTime'] = response.xpath('//li[@class="ellipsis"][3]/text()').extract()[0]

        # 对加密数据的处理部分
        dhtml = response.xpath('*').extract()[0]
        # 下载字体文件
        woff = regex_woff.search(dhtml).group()
        wofflink = 'http:' + woff
        localname = 'fonts/' + os.path.basename(wofflink)
        if not os.path.exists(localname):
            downloads(wofflink, localname)
        font = TTFont(localname)

        # 其中含有 unicode 字符，用原始文本通过正则获取
        ms = regex_text.findall(dhtml)
        if len(ms) < 3:
            item['rate'] = '0'
            item['rateNum'] = '0'
            item['boxOffice'] = '0'
        else:
            item['rate'] = get_fontnumber(font, ms[0])
            item['rateNum'] = get_fontnumber(font, ms[1])
            item['boxOffice'] = (
                        get_fontnumber(font, ms[2]) + response.xpath('//span[@class="unit"]/text()').extract()[0])

        yield item
