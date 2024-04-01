import requests
import json

url = "https://api.foursquare.com/v3/places/search"

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3X3b+iP8ctVXBzIYZDzTL44Y3VduKCgUMNviQmkPGkMU="
}

city = input('Enter city name - ')
category = input('Enter category name - ')
params = {
  	"query": category,
  	"near": city,
  	"sort": "rating"
}

response = requests.get(url, headers=headers, params=params)
if response.ok:
    with open('response.json', 'w', encoding='UTF-8') as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)

    data = response.json()
    print()
    for value in data['results']:
        try:
            if value['location']['address']:
                print(f"Название - {value['name']}")
                print(f"Адрес - {value['location']['address']}")
        except:
            continue
        print()
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)



