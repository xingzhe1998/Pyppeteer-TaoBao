# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class TaobaoPipeline(object):
    def process_item(self, item, spider):
        item['commodity_shop_url'] = 'https:' + item['commodity_shop_url'] if not item['commodity_shop_url'].startswith('https:') else item['commodity_shop_url']
        item['commodity_detail_url'] = 'https:' + item['commodity_detail_url'] if not item['commodity_detail_url'].startswith('https:') else item['commodity_detail_url']
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        print('正在插入数据到mongodb...')
        self.db['tb_info'].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

