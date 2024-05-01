# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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

