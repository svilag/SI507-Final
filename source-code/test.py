import requests
import re
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs

url = 'https://wgi.org/percussion/perc-scores-2020/'
req = requests.get(url).text

soup = bs(req, 'html.parser')
table_rows = soup.find_all('tr') # list

@dataclass(frozen=True)
class Competition:
    """creates a competition class object"""
    title: str
    date: str
    scores: str
    recap: str

# comps = []
# for tr in table_rows: # find tr tags
#     tr_children = [child for child in tr.children] # find children
#     if len(tr_children) == 9: # grab only lines with score data linked
#         tr_children_data = tr_children[1::2][1:]
#         comp_name = tr_children_data[0].contents # get competition name # list len 0
#         scores = tr_children_data[1].a['href'] # get link to scores
#         recaps = tr_children_data[-1].a['href'] # get link to recaps
#         competition = {'competition': comp_name[0], 'scores': scores, 'recaps': recaps}
#         comps.append(competition)

# print(comps[0])

# x = {'competition': comp_name, 'date': date, 'scores': scores, 'recap': recaps}
comp_list = []
class_list = []
for tr in table_rows[:-1]:
    comps = {}
    tr_children = [child for child in tr.children] # find children
    if len(tr_children) == 3: # rows with dates
        date = tr_children[1:-1:1][0].strong.contents[0]
    elif len(tr_children) == 9:
        tr_children_data = tr_children[1::2][1:]
        comp_name = tr_children_data[0].contents # get competition name # list len 0
        scores = tr_children_data[1].a['href'] # get link to scores
        recaps = tr_children_data[-1].a['href'] # get link to recaps
        # competition = {'competition': comp_name[0], 'scores': scores, 'recaps': recaps}
        # comps[date].append(competition)
        comps['competition'] = comp_name[0]
        comps['date'] = date
        comps['scores'] = scores
        comps['recap'] = recaps
        comp_list.append(comps)
        competition = Competition(comp_name[0], date, scores, recaps)
        class_list.append(competition)

print(class_list[0])



