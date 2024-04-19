import scrapy
from scrapy.http import HtmlResponse
from unsplashparser.unsplashparser.items import UnsplashparserItem
from scrapy.loader import ItemLoader

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        categorys = response.xpath("//li/a[contains(@href, '/t/')]")
        for category in categorys[:1]:
            yield response.follow(category, callback=self.parse)
        photo_links = response.xpath('//div/a[@itemprop="contentUrl"]/@href')
        for link in photo_links[:2]:
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        photo = response.xpath("//div[@class='WxXog']/img/@src").get()
        category = response.xpath('//span[@class="jmdKh"]/a/text()').get()
        yield UnsplashparserItem(name=name, photo=photo, category=category)