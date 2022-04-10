import requests
import re
from bs4 import BeautifulSoup as bs

url = 'https://wgi.org/percussion/perc-scores-2020/'
req = requests.get(url).text

soup = bs(req, 'html.parser')
table_rows = soup.find_all('tr') # list

recap = soup.find_all(string=re.compile("Recap"))
print(recap)



