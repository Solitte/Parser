from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017)
db = client['toscrape_books']
books = db['books']

books.delete_many({})

with open('all_books.json', 'r', encoding='UTF-8') as f:
    data = json.load(f)

batch = 100

for i in range(0, len(data), batch):
    books.insert_many(data[i:i + batch])

query = books.find({'description': 'No description'})
print("Book with no description:")
for book in query:
    print(book['name'])
print(f"Count books with no description: {books.count_documents({'description': 'No description'})}")
print()

print("Books whose price is more than 30 pounds and whose remainder is more than 20 pieces: ")
for book in books.find({'stock': {'$gt': 17}}):
    if float(book['price'][1:]) > 50:
        print(f"Name - {book['name']}, Price - {book['price']}, Stock - {book['stock']}")
