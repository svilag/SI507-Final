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


BASE_URL = 'https://wgi.org'
# PERCUSSION_URL = 'percussion/'
# GUARD_URL = 'color-guard/'
# WINDS_URL = 'winds/'



# Classes

@dataclass(frozen=True)
class Percussion:
    """creates a percussion class object"""
    group_type: str
    name: str

@dataclass(frozen=True)
class Guard:
    """creates a color guard class object"""
    group_type: str
    name: str

@dataclass(frozen=True)
class Winds:
    """creates a winds class object"""
    group_type: str
    name: str






# Functions

def read_json():

def cache_pages():
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

def get_competition_data(data):
    """ takes in a url to a page with a list of competitions with links to their score data
        and returns a list of dicts of each competition name and links to the scores and recap pages.

    params:
        data: link to html content

    returns:
        comps(list): list of dicts [{'competition': comp_name, 'scores': link, 'recaps': link},...]
    """
    soup = bs(data, 'html.parser')
    table_rows = soup.find_all('tr')
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

    return comps





if __name__ == '__main__':
    print('program started')
