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

@dataclass(frozen=True)
class Competition:
    """creates a competition class object"""
    title: str
    date: str
    scores: dict
    recap: str
    groups: list






# Functions

def read_json(filepath, encoding='utf-8'):
    """Reads a json file and returns a dictionary of the object
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def soup(url):
    """takes a url and returns a BS4 response
    """
    req = requests.get(url).text
    stew = bs(req, 'html.parser')

    return stew

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
        comps(list): list of Competition objects
    """
    





if __name__ == '__main__':
    print('program started')
    links = read_json(URLS)
    for link in links:
        response = soup(link)
        

