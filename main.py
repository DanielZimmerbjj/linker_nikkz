import requests_html
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

session = requests_html.HTMLSession()
r = session.get('https://nic.kz/')
about = r.html.find('#last-ten-table', first=True)

with open(f'links.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter='\n', lineterminator='\r')
    writer.writerows(
        [about.absolute_links]
    )

df = pd.read_csv(f'links.csv',
                 names=['name'],
                 engine='python', encoding='utf-8')
df.drop_duplicates(subset=['name']).to_csv(f'links.csv', header=None, index=False, )

f = open('links.csv')
i = 0
for line in f:
    i+=1
print('всего собрано уникальных ссылок:', i)



