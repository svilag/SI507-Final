import requests
import re
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs


@dataclass(frozen=True)
class Group:
    """creates a group class object"""
    group_type: str
    name: str
    class_level: str
    location: str

@dataclass(frozen=True)
class Competition:
    """creates a competition class object"""
    title: str
    date: str
    scores: dict
    recap: str
    groups: list


def soup(url):
    """takes a url and returns a BS4 response
    """
    req = requests.get(url).text
    stew = bs(req, 'html.parser')

    return stew

url = 'https://wgi.org/percussion/perc-scores-2020/'
req = requests.get(url).text
soupy = soup(url)
table_rows = soupy.find_all('tr') # list

# x = {'competition': comp_name, 'date': date, 'scores': scores, 'recap': recaps}
comp_list = [] # [{'competition': comp_name, 'date': date, 'scores': scores, 'recap': recaps},...]
for tr in table_rows[:-1]:
    comps = []
    tr_children = [child for child in tr.children] # find children
    if len(tr_children) == 3: # rows with dates
        date = tr_children[1:-1:1][0].strong.contents[0]
    elif len(tr_children) == 9:
        tr_children_data = tr_children[1::2][1:]
        comp_name = tr_children_data[0].contents # get competition name # list
        scores = tr_children_data[1].a['href'] # get link to scores
        recaps = tr_children_data[-1].a['href'] # get link to recaps

        print(scores)
        groups = []
        scores_data = soup(scores)
        rows = scores_data.find_all('tr') # list
        
        # TODO get list of groups
        # TODO create dict of scores
        # TODO create Group class objects


    # TODO create Competition class objects




