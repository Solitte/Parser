import requests
from lxml import html
import csv


url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
session = requests.session()
list_news = []
response = session.get(url, headers=headers)
if response.ok:
    dom = html.fromstring(response.content)
    daynews = dom.xpath("//div[contains(@class, 'daynews')]/span[contains(@class, 'photo phot')]")
    othernews = dom.xpath("//ul[@data-module='TrackBlocks']/li[@class='list__item']//a")
    for news in daynews:
        dict_news = {}
        name = news.xpath("./span/span/text()")
        link = news.xpath("./a/@href")
        if len(name) > 1:
            dict_news['name'] = '. '.join(name).replace('\xa0', ' ')
        else:
            dict_news['name'] = name[0].replace('\xa0', ' ')
        dict_news['link'] = link[0]
        list_news.append(dict_news)
    for news in othernews:
        dict_news = {}
        name = news.xpath("text()")
        link = news.xpath("@href")
        dict_news['name'] = name[0]
        dict_news['link'] = link[0]
        list_news.append(dict_news)

    print(list_news)
    with open('Topnews.csv', 'w', encoding='UTF-8') as f:
        writer = csv.DictWriter(
            f, fieldnames=list(list_news[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for data in list_news:
            writer.writerow(data)
else:
    print('Error load page')

