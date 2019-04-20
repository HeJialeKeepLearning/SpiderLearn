# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class top100Pipeline(object):
    def process_item(self, item, spider):
        with open('maoyanTop100.txt', 'a', encoding = 'utf8') as fp:
            fp.write('电影名:' + str(item['name']) + '\t' + str(item['stars'])
                     + '\t' + str(item['releaseTime']) + '\t评分:' + str(item['rate'])
                     + '\t海报url:' + str(item['poster']) + '\n')

class moviePipeline(object):
    movieInsert = '''insert into maoyanMovie(id,name,poster) values ('{id}','{name}','{poster}')'''

    def open_spider(self, spider):
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

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        id = item['id']
        sql = 'select * from maoyanMovie where id=%s' % id
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:  # 该表项存在
            name = item['name']
            poster = item['poster']
            sql = 'update maoyanMovie set name=%s,poster=%s where id =%s' % (name, repr(poster), id)
            self.cursor.execute(sql)
        else:
            sqlinsert = self.movieInsert.format(
                id = item['id'],
                name = pymysql.escape_string(item['name']),
                poster = pymysql.escape_string(item['poster'])
            )
            self.cursor.execute(sqlinsert)
        return item

class movieInfoPipeline(object):

    def open_spider(self, spider):
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

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        id = item['id']
        stars = item['stars']
        releaseTime = item['releaseTime']
        rate = item['rate']
        rateNum = item['rateNum']
        boxOffice = item['boxOffice']
        sql = 'update maoyanMovie set ' \
              'stars=%s,releaseTime=%s,rate=%s,rateNum=%s,boxOffice=%s' \
              ' where id =%s' % (repr(stars), repr(releaseTime), repr(rate), repr(rateNum), repr(boxOffice), id)
        self.cursor.execute(sql)

        return item

class boxOfficePipeline(object):
    boxOfficeInsert = '''insert into maoyanBoxoffice(movieId,movieName,sumBoxInfo,boxInfo,boxRate,showRate,avgSeatView,avgShowView) 
        values ('{movieId}','{movieName}','{sumBoxInfo}','{boxInfo}','{boxRate}','{showRate}','{avgSeatView}','{avgShowView}')'''

    def open_spider(self, spider):
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

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        movieId = item['movieId']
        sql = 'select * from maoyanBoxoffice where movieId=%s' % movieId
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:  # 该表项存在
            avgSeatView=item['avgSeatView']
            avgShowView=item['avgShowView']
            boxInfo=item['boxInfo']
            boxRate=item['boxRate']
            sumBoxInfo=item['sumBoxInfo']
            showRate=item['showRate']
            sql = 'update maoyanMovie set ' \
                  'avgSeatView=%s,avgShowView=%s,boxInfo=%s,boxRate=%s,sumBoxInfo=%s,showRate=%s' \
                  ' where id =%s' % (repr(avgSeatView), repr(avgShowView),repr(boxInfo),repr(boxRate),repr(sumBoxInfo),repr(showRate), movieId)
            self.cursor.execute(sql)
        else:
            sqlinsert = self.boxOfficeInsert.format(
                movieId = pymysql.escape_string(item['movieId']),
                movieName = pymysql.escape_string(item['movieName']),
                sumBoxInfo = pymysql.escape_string(item['sumBoxInfo']),
                boxInfo = pymysql.escape_string(item['boxInfo']),
                boxRate = pymysql.escape_string(item['boxRate']),
                showRate = pymysql.escape_string(item['showRate']),
                avgSeatView = pymysql.escape_string(item['avgSeatView']),
                avgShowView = pymysql.escape_string(item['avgShowView'])
            )
            self.cursor.execute(sqlinsert)
        return item
