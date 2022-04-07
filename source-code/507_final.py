"""
This program parses scores from https://wgi.org
"""
from dataclasses import dataclass
import json
import Flask
import requests
import re
import sys
from bs4 import BeautifulSoup


BASE_URL = 'https://wgi.org'
# PERCUSSION_URL = 'percussion/'
# GUARD_URL = 'color-guard/'
# WINDS_URL = 'winds/'

url_paths = {'percussion/', 'color-guard/', 'winds/'}
score_years = {2018, 2019, 2020, 2021, 2022}

# url patterns:
# yyyy-perc-scores
# perc-scores-yyyy
# yyyy-percussion-scores

def cache_pages():
    """parses pages on wgi.com with scores data and caches the pages

    params:
        url(string): url to cache

    returns:
        cache
    """
    # TODO implement caching
    for path in url_paths:
        url = BASE_URL + path
        for year in score_years:
            try:
                data = requests.get
            finally:
                data = requests.get
            # TODO

def parse_scores(data):
    """parses pages on wgi.com with scores data"""
    # TODO implement parser
    pass


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



if __name__ == '__main__':
    print('program started')
