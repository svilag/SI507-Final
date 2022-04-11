import requests
import re
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs


@dataclass(frozen=True)
class Group:
    """creates a group class object"""
    # group_type: str
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

        # print(scores)
        scores_data = soup(scores)
        scores_div = scores_data.find_all('div', attrs={'class': 'table-responsive'}) # list of div elements # len = 1

        all_groups = []
        groups = {} # {class_lvl: [group, group,...], class_lvl: [...]}
        scores= {} # {group: score, ...}

        scores_table = scores_div[0].table # .table.tbody.tr.td.table
        table_rows = scores_table.find_all('tr')
        for row in table_rows:
            tcells = [child for child in row.children]
            # print(len(tcells))
            # print(tcells[2])
            if len(tcells) == 3:
                class_level = tcells[1].b.contents[0] # group class_level
                class_groups = []
            elif len(tcells) == 4:
                em = tcells[2].contents[1]
                group_name = tcells[2].contents[0].strip() # group names
                location = em.contents[0].replace('(', '').replace(')', '') # group location

                group = Group(group_name, class_level, location) # create Group class object
                all_groups.append(group) # add group to all groups for that competition
                class_groups.append(group) # add group to list for that class_lvl

                score = tcells[-1].b.contents[0]
                scores[group_name] = score

            groups[class_level] = class_groups

        competition = Competition(comp_name[0], date, scores, recaps, groups) # create Competition class object

