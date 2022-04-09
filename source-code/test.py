import requests
from bs4 import BeautifulSoup as bs

url = 'https://wgi.org/percussion/perc-scores-2020/'
req = requests.get(url).text

soup = bs(req, 'html.parser')
table_rows = soup.findAll('tr')

print(table_rows)
