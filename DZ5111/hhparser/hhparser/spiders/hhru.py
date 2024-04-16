import scrapy
from scrapy.http import HtmlResponse
from hhparser.items import HhparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls =['https://ufa.hh.ru/search/vacancy?text=Python&from=suggest_post&area=99&hhtmFrom=main&hhtmFromLabel=vacancy_search_line']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-ControlsNext::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serpitem__row_header a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        salary = response.css('div.vacancy-title p.vacancysalary::text').extract()
        # print(name, salary)
        yield HhparserItem(name=name, salary=salary)
