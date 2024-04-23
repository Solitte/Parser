import scrapy
from scrapy.http import HtmlResponse
from unsplashparser.unsplashparser.items import UnsplashparserItem
from scrapy.loader import ItemLoader

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    # def __init__(self, mark):
    #     self.start_urls = [f'https://unsplash.com/s/photos/{mark}']

    def parse(self, response):
        categorys = response.xpath("//li/a[contains(@href, '/t/')]")
        for category in categorys:
            yield response.follow(category, callback=self.parse)
        photo_links = response.xpath('//div/a[@itemprop="contentUrl"]/@href')
        for link in photo_links:
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        photo = response.xpath("//div[@class='WxXog']/img/@src").get()
        category = response.xpath('//span[@class="jmdKh"]/a/text()').get()
        yield UnsplashparserItem(name=name, photo=photo, category=category)
