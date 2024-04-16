# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class HhparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_ufa

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        if item['salary']:
            salary_ = ''.join(item['salary'])
            salary_ = salary_.replace('₽', 'руб')
            if item['salary']:
                for i in range(len(item['salary'])):
                    if 'от' in item['salary'][i]:
                        item['min_salary'] = int(item['salary'][i + 1].replace(' ', ''))
                    if 'до' in item['salary'][i] and 'вычета' not in item['salary'][i] :
                        item['max_salary'] = int(item['salary'][i + 1].replace(' ', ''))
                        break
            item['salary'] = salary_
        else:
            item['salary'] = 'По договоренности'
        collection.insert_one(item)
        return item
