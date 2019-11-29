# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import re



class MongoDBPipeline():
    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class CustomTextParsePipeline:
    def process_item(self, item, spider):
        item['name'] = self.parse_text(item['name']).replace('/', '-')
        item['price'] = self.parse_price(item['price'])
        item['vendor'] = self.parse_text(item['vendor'])
        return item

    @staticmethod
    def parse_text(text):
        try:
            clean = re.sub('s/^\s+|\s+$|\s+(?=\s)', '', text)
            clean = clean[1:] if clean[0] == ' ' else clean
            return clean
        except:
            return ''

    @staticmethod
    def parse_price(price):
        try:
            return re.findall('\d+', price)[0]
        except:
            return ''


class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield scrapy.Request(image_url, meta={'category': item.get('category'), 'name': item.get('name')})

    def file_path(self, request, response=None, info=None):
        category, name = request.meta.get('category'), request.meta.get('name')
        return 'full/{}/{}.jpg'.format(category, name)

