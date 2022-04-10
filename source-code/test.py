import requests
import re
from bs4 import BeautifulSoup as bs

url = 'https://wgi.org/percussion/perc-scores-2020/'
req = requests.get(url).text

soup = bs(req, 'html.parser')
table_rows = soup.find_all('tr') # list

comps = []
for tr in table_rows: # find tr tags
    tr_children = [child for child in tr.children] # find children
    if len(tr_children) == 9: # grab only lines with score data linked
        tr_children_data = tr_children[1::2][1:]
        comp_name = tr_children_data[0].contents # get competition name # list len 0
        scores = tr_children_data[1].a['href'] # get link to scores
        recaps = tr_children_data[-1].a['href'] # get link to recaps
        competition = {'competition': comp_name[0], 'scores': scores, 'recaps': recaps}
        comps.append(competition)

print(comps[0])

