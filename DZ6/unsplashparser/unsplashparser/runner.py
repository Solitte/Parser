from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from unsplashparser.unsplashparser.spiders.unsplash import UnsplashSpider


if __name__ == '__main__':
    configure_logging()
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    # mark = input()
    process = CrawlerProcess(get_project_settings())
    process.crawl(UnsplashSpider)
    process.start()
