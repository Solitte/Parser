import scrapy
from scrapy.http import HtmlResponse
from hhparser.hhparser.items import HhparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls =['https://ufa.hh.ru/search/vacancy?text=Python&from=suggest_post&area=99&hhtmFrom=main&hhtmFromLabel=vacancy_search_line']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacansy = response.xpath("//span[@class='serp-item__title-link-wrapper']//@href").getall()
        print(vacansy)
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").getall()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield HhparserItem(name=name, salary=salary, url=url)
