# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Spiderl2DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class moviePipeline(object):
    def process_item(self,item,spider):
        with open('doubanMovie.txt', 'a', encoding = 'utf8') as fp:
            fp.write(str(item['id']) + '\t'+str(item['title'])+'\t'+str(item['rating'])+'\t'
                     +str(item['alt']) + '\t'+str(item['image']) + '\t\n')

class reviewPipeline(object):
    def process_item(self,item,spider):
        return item