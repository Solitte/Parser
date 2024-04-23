from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import json
import time
import random

input_user = input('Search at OZON - ') #"платье 100% лен"

options = Options()
options.add_argument('--start-maximized')
options.add_argument('--deny-permission-prompts')
driver = uc.Chrome(options=options)
driver.get("https://www.ozon.ru/")


items_list = []

wait = WebDriverWait(driver, 30)
input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Искать на Ozon"]')))
input.send_keys(input_user + '\n')
count = 0
filter = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@text="Популярные"]')))
actions = ActionChains(driver)
time.sleep(5)
actions.move_to_element(filter).perform()
actions.move_to_element(filter).click(filter).send_keys(Keys.DOWN).send_keys(Keys.ENTER)
actions.perform()

while True:
    count += 1
    time.sleep(5 + random.randint(1, 5))
    try:
        start_next_pages = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="b210-a8 tsBodyControl400Small"]')))
        items = driver.find_elements(By.XPATH, '//div[@class="i4x i5x tile-root"]')
    except:
        break
    for item in items:
        try:
            name = item.find_element(By.XPATH,'.//span[@class="tsBody500Medium"]').text
        except:
            name = ''
        try:
            price = item.find_element(By.XPATH, './/div[@class="c302-a0"]/span').text
            price = int(''.join(price.split()[:-1]))
        except:
            price = 0
        try:
            url = item.find_element(By.XPATH, './/div[@class="xi6"]/a').get_attribute('href')
        except:
            url = ''
        items_list.append({'name': name, 'price': price, 'url': url})
    if (len(start_next_pages) == 1 and start_next_pages[0].text == 'В начало') or not start_next_pages:
        print(f'Last Page {count}')
        break
    for pages in start_next_pages:
        if pages.text == 'Дальше':
            actions.scroll_to_element(pages).perform()
            actions.move_to_element(pages).perform()
            actions.scroll_to_element(pages).move_to_element(pages).click(pages)
            actions.perform()
            print(f'Next Page {count+1}')

with open(f'{input_user}.json', 'w', encoding='UTF-8') as f:
    json.dump(items_list, f, indent=4, ensure_ascii=False)

