import requests
from bs4 import BeautifulSoup
import json


url = 'https://www.g2g.com/offer/Gehennas--EU----Horde'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
params = 'service_id=lgc_service_1&brand_id=lgc_game_29076&region_id=ac3f85c1-7562-437e-b125-e89576b9a38e&fa=lgc_29076_server%3Algc_29076_server_41023'
params_list = params.split('&')
params_dict = {}
for param in params_list:
    params_dict[param.split('=')[0]] = param.split('=')[1]
session = requests.session()
response = session.get(url, headers=headers, params=params_dict)
if response.ok:
    price =[]
    soup = BeautifulSoup(response.content, 'html.parser')
    offers = soup.find_all('div', {'class': 'other_offer-desk-main-box other_offer-div-box'})
    for offer in offers:
        seller = offer.find('div', {'class': 'seller__name-detail'}).getText()
        print(seller)
        if seller == 'EternalStock':
            price.append(offer.find('span', {'class': 'offer-price-amount'}).getText())
    print(price)
    # s=0
    # for i in price:
    #     s+=float(i)
    # mean=s/len(price)
    # print(mean)
