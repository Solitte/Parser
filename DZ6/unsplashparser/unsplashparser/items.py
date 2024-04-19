# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    photo = scrapy.Field()
    pass
