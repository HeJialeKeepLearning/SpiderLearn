# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class top100Pipeline(object):
    def process_item(self, item, spider):
        with open('maoyanTop100.txt', 'a', encoding = 'utf8') as fp:
            fp.write('电影名:' + str(item['name']) + '\t' + str(item['stars'])
                     + '\t' + str(item['releaseTime']) + '\t评分:' + str(item['rate'])
                     + '\t海报url:' + str(item['poster']) + '\n')

class moviePipeline(object):
    def process_item(self, item, spider):
        with open('maoyanMovieId.txt', 'a', encoding = 'utf8') as fp:
            fp.write(str(item['id']) + '\n')
