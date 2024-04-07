from clickhouse_driver import Client
import json


client = Client('localhost')

client.execute('CREATE DATABASE IF NOT EXISTS toscrape_books_click')


client.execute('''
CREATE TABLE IF NOT EXISTS toscrape_books_click.books (
    id Int64,
    name String,
    price String,
    stock Int64,
    description String    
) ENGINE = MergeTree()
ORDER BY id
''')

print("Таблица создана успешно.")

with open('all_books.json', 'r', encoding='UTF-8') as f:
    data = json.load(f)

id = 1
for i in data:

    client.execute("""
    INSERT INTO toscrape_books_click.books (
        id, name, price,
        stock, description
    ) VALUES""",
    [(id,
      i['name'] or "",
      i['price'] or "",
      i['stock'],
      i['description']
      )])
    id += 1

print("Данные введены успешно.")


result = client.execute("SELECT * FROM toscrape_books_click.books")
print("Вставленная запись:", result[0])
