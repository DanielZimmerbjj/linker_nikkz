# сбор емайл с сайта nic.kz (первая работа)
import requests
import requests_html
from bs4 import BeautifulSoup
import json
import time
import csv
import pandas as pd
import os

timestr = time.strftime("%Y-%m-%d")

# парсинг ссылок с сайта nic.kz
session = requests_html.HTMLSession()
r = session.get('https://nic.kz/')
about = r.html.find('#last-ten-table', first=True)

with open(timestr+'_links.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter='\n', lineterminator='\r')
    writer.writerows(
        [about.absolute_links]
    )
# поиск дубликатов ссылок
df = pd.read_csv(timestr+'_links.csv',
                 names=['name'],
                 engine='python', encoding='utf-8')
df.drop_duplicates(subset=['name']).to_csv(timestr+'_links.csv', header=None, index=False, )

f = open(timestr+'_links.csv')
i = 0
for line in f:
    i += 1
print('Всего собрано уникальных ссылок:', i)

with open(timestr+'_links.csv') as file:

    lines = [line.strip() for line in file.readlines()]

    data_dict = []
    count = 0
# поиск таблицы с данными
for line in lines:
    q = requests.get(line)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')
    data = soup.find('pre').text
    domain_data = data.strip().split('\n')

    data = {
        'domain_data': domain_data,
        }
    count += 1
    print(f'#{count}: {line} Данные собраны!')

    data_dict.append(data)
# сохранение таблицы в файл json
with open('data.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=0)


# сбор почтовых адресов из файла data.json

mail = u'"Email Address..........: '

with open('data.json', encoding='utf-8') as file1:
    with open(timestr+"_mail.txt", "w") as file:
        for line in file1:
            if mail in line:
                email = line\
                    .replace('"Email Address..........: ', '',)\
                    .replace('"', '',)\
                    .replace('hostmaster@hoster.kz,', '',) \
                    .replace('billing@hoster.kz,', '', ) \
                    .replace("\n", "")\
                    .replace(",", "\n")

                file.writelines(email)
os.remove("data.json")
# удаляем дубликаты email
file = timestr+'_mail.txt'
uniqlines = set(open(file, 'r', encoding='utf-8').readlines())
done = open(file, 'w', encoding='utf-8').writelines(set(uniqlines))

# считаем строки в файле(email)
f = open(timestr+'_mail.txt')
i = 0
for line in f:
    i += 1
print('Сегодня собрано уникальных email:', i)
