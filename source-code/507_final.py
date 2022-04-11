"""
This program parses scores from https://wgi.org
"""
from dataclasses import dataclass
import json
import Flask
import requests
import re
import sys
from bs4 import BeautifulSoup as bs

URLS = "./urls.json"

# Classes
# using Frozen=True so classes cannot be edited once instantiated

@dataclass(frozen=True)
class Group:
    """creates a group class object"""
    group_type: str
    name: str

# @dataclass(frozen=True)
# class Guard:
#     """creates a color guard class object"""
#     group_type: str
#     name: str

# @dataclass(frozen=True)
# class Winds:
#     """creates a winds class object"""
#     group_type: str
#     name: str

@dataclass(frozen=True)
class Competition:
    """creates a competition class object"""
    title: str
    date: str
    scores: str
    recap: str




# Functions

def read_json(filepath, encoding='utf-8'):
    """Reads a json file and returns a dictionary of the object
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def cache_pages(url):
    """parses pages on wgi.com with scores data and caches the pages

    params:
        url(string): url to cache

    returns:
        cache
    """
    # TODO implement caching
    pass

def get_score_recap(data):
    """parses pages on wgi.com with scores data"""
    pass

def get_competitions(data):
    """ takes in a url to a page with a list of competitions with links to their score data
        and returns a list of dicts of each competition name and links to the scores and recap pages.

    params:
        data: link to html content

    returns:
        comps(list): list of comp objects [{'competition': comp_name, 'scores': link, 'recaps': link},...]
    """
    soup = bs(data, 'html.parser')
    table_rows = soup.find_all('tr')

    comp_list = [] # [{'competition': comp_name, 'date': date, 'scores': scores, 'recap': recaps},...]
    for tr in table_rows[:-1]:
        comps = []
        tr_children = [child for child in tr.children] # find children
        if len(tr_children) == 3: # rows with dates
            date = tr_children[1:-1:1][0].strong.contents[0]
        elif len(tr_children) == 9:
            tr_children_data = tr_children[1::2][1:]
            comp_name = tr_children_data[0].contents # get competition name # list len 0
            scores = tr_children_data[1].a['href'] # get link to scores
            recaps = tr_children_data[-1].a['href'] # get link to recaps
            comp_list.append(comps)
            competition = Competition(comp_name[0], date, scores, recaps)
            comps.append(competition)

    return comps





if __name__ == '__main__':
    print('program started')
