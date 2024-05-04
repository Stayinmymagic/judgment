# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import mysql.connector
import json
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('proxy_list.json', 'w+')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()
    
class JudgmentPipeline:
    def open_spider(self, spider):
        uri = spider.settings.get('MONGODB')
        db_name = spider.settings.get('MONGODB_NAME')
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]

    def process_item(self, item, spider):
        self.insert_item(item)
        return item
    
    def insert_item(self, item):
        item = dict(item)
        self.db.proxy.insert_one(item)

    def close_spider(self,spider):
        self.client.close()
class AgeFilterPipeline:
    def process_item(self, item, spider):
        if item['event_age'] < 20:
            raise DropItem(f"年紀小於 20")
        return item
class DropDuplicatesPipeline:
    def __init__(self):
        self.article = set()
    def process_item(self, item, spider):
        link = item['link'] 
        if link in self.article:
            raise DropItem('duplicates link found %s', item)
        self.article.add(link)
        return item


class SavePipeline:   
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
        host=spider.settings.get('MYSQLDB_HOST'),# 主機名稱
        database=spider.settings.get('MYSQLDB_NAME'), # 資料庫名稱
        user=spider.settings.get('MYSQLDB_USER'),        # 帳號
        password=spider.settings.get('MYSQLDB_PWD'))  # 密碼

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item
    
    def insert_item(self, item):
        self.cur.execute("""INSERT INTO scrapy_history VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (
                                item['pid'],item['name'],item['court'],item['crime_type'],item['event_time'],item['event_age'],
                                item['amount'],item['company'],item['map_family'],item['map_address'],item['link'], datetime.now().strftime("%Y-%m-%d")
                            ))

        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cur.close()

