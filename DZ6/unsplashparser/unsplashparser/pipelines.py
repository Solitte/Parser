# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class UnsplashparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.unsplash_photo
        self.items = []
    def open_spider(self, spider):
        self.file = open('data.csv', 'w')


    def close_spider(self, spider):
        writer = csv.DictWriter(
            self.file, fieldnames=list(self.items[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for item in self.items:
            writer.writerow(item)
        self.file.close()

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        item['photo_path'] = item['photo'][0]['path']
        item['photo']=item['photo'][0]['url']
        collection.insert_one(item)
        self.items.append(item)
        return item


class UnsplashphotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)


    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item



