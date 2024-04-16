import requests
from lxml import html
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
list_orders = []
if response.ok:
    dom = html.fromstring(response.content)
    orders = dom.xpath("//div[@class='other_offer-desk-main-box other_offer-div-box']")
    for order in orders:
        dict_orders = {}
        seller_name = order.xpath(".//div[@class='seller__name-detail']/text()")
        seller_price = order.xpath(".//span[contains(@class,'price')]/text()")
        dict_orders['seller_name'] = seller_name[0]
        dict_orders['seller_price'] = seller_price[0]
        list_orders.append(dict_orders)

    print(list_orders)
    with open('Gehenas.json', 'w', encoding='UTF-8') as f:
        json.dump(list_orders, f, indent=4)
else:
    print('Error load page')

