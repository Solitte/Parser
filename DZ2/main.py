import requests
from bs4 import BeautifulSoup
import json


url = 'http://books.toscrape.com/catalogue/'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
session = requests.session()
list_href = []
i = 1
while True:
    page = f'page-{i}.html'
    response = session.get(url + page, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            list_href.append(url + book.find('a').get('href'))
        print(f'Page {i}')
    else:
        break
    i += 1
all_books = []
count = 0
for href in list_href:
    print(f'Book number {count}')
    count += 1
    book = {}
    response = session.get(href, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        info_book = soup.find('div', {'class': 'col-sm-6 product_main'})
        book['name'] = info_book.findChild('h1').getText()
        book['price'] = info_book.find('p', {'class': 'price_color'}).getText()
        stock = info_book.find('p', {'class': 'instock availability'}).getText()
        book['stock'] = int(stock[stock.find('(')+1:stock.find('(') + 1 + stock.find(' ')])
        try:
            book['description'] = soup.find('article', {'class': 'product_page'}).find('p', {'class': ''}).getText()
        except:
            book['description'] = 'No description'
        all_books.append(book)

print(len(all_books))
with open('all_books.json', 'w', encoding='UTF-8') as f:
    json.dump(all_books, f, indent=4)
