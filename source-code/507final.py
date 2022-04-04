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
PERCUSSION_URL = 'percussion/'
GUARD_URL = 'color-guard/'
WINDS_URL = 'winds/'

score_years = {2018, 2019, 2020, 2021, 2022}

# url patterns:
# yyyy-perc-scores
# perc-scores-yyyy
# yyyy-percussion-scores


@dataclass()
class Percussion:



if __name__ == '__main__':
    print('program started')
