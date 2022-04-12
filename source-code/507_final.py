"""
This program parses scores from https://wgi.org
"""
from dataclasses import dataclass
import json
import logging
import os
import re
import sys
import datetime as dt
from flask import Flask, Response
import requests
from bs4 import BeautifulSoup as bs

URLS = "./urls.json"
CACHE = {}

# Classes
# using Frozen=True so classes cannot be edited once instantiated

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






# Functions

def read_json(filepath, encoding='utf-8'):
    """Reads a json file and returns a dictionary of the object
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2, add=False):
    """ Serializes object as JSON. Writes content to the provided filepath.
        Appends to the end of the file. Checks if filepath exists.
        If not, appends file creating a new one if the file does not exists,
        else writes over the file. If add=True, appends to the end of the file.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON
        add (optional): optional parameter to tell the function to append to the end of the file

    Returns:
        None
    """
    if not os.path.exists(filepath):
        with open(filepath, 'a', encoding=encoding) as file_obj:
            json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
    else:
        if add is False:
            with open(filepath, 'w', encoding=encoding) as file_obj:
                json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
        else:
            with open(filepath, 'a', encoding=encoding) as file_obj:
                json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def stew(url: str) -> bs:
    """takes a url and returns a BS4 response

    params:
        url(str): link to html content

    returns:
        meal: BeautifulSoup object
    """
    req = requests.get(url).text
    meal = bs(req, 'html.parser')

    return meal

def get_content(url: str) -> str:
    """Takes a url and returns the html content

    params:
        url(string): link to html content

    returns:
        response.text: html content
    """
    response = requests.get(url)

    return response.text

def check_cache(url: str) -> str:
    """ checks if a url is already in the cache. if not, adds it.
        Also writes the cache to a JSON file.

    params:
        url(str): url

    returns:
        CACHE[url]: contents from the html page
    """
    if url not in CACHE:
        CACHE[url] = get_content(url)
        logging.info("%s added to cache", url)

    write_json('./cache/cache.json', CACHE)
    return CACHE[url]







# def get_score_recap(data):
#     """parses pages on wgi.com with scores data"""
#     pass
# TODO parse score recap pages

def get_competitions(data):
    """ takes a url to a page with a list of competitions with links to their score data, parses the scores page and
        creates Competition and Group objects. Writes these objects to JSON files.

    params:
        data(str): link to html content
    """
    cache_data = check_cache(data) # check cache for url content
    logging.info("Checking cache for %s", data)

    # soupy = stew(data)
    soupy = bs(cache_data, 'html.parser') # read from cache
    logger.info("Parsing page: %s", data) # log url

    table_rows = soupy.find_all('tr') # list


    comps_to_write = [] # Competition objects as json
    groups_to_write = [] # Group objects as json

    for t_r in table_rows[:-1]:
        tr_children = [child for child in t_r.children] # find children
        if len(tr_children) == 3: # rows with dates
            date = tr_children[1:-1:1][0].strong.contents[0]
        elif len(tr_children) == 9:
            tr_children_data = tr_children[1::2][1:]
            comp_name = tr_children_data[0].contents # get competition name # list
            scores = tr_children_data[1].a['href'] # get link to scores # TODO debug
            recaps = tr_children_data[-1].a['href'] # get link to recaps


            # TODO reorganize into get_scores()
            # TODO assign url to scores or None
            # TODO update class data
            # TODO update schema
            # print(scores)
            scores_data = stew(scores) # follow link to scores page
            scores_div = scores_data.find_all('div', attrs={'class': 'table-responsive'}) # list of div elements # len = 1

            all_groups = [] # all groups at the competition
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
                    class_groups = [] # groups in this class level
                elif len(tcells) == 4:
                    em = tcells[2].contents[1]
                    group_name = tcells[2].contents[0].strip() # group names
                    location = em.contents[0].replace('(', '').replace(')', '') # group location

                    group = Group(group_name, class_level, location) # create Group class object

                    group_json = {
                        "name": group.name,
                        "class_level": group.class_level,
                        "location": group.location
                    }

                    if group_json not in groups_to_write: # check if group in list; add if not
                        groups_to_write.append(group_json)

                    all_groups.append(group) # add group to all groups for that competition
                    class_groups.append(group) # add group to list for that class_lvl

                    score = tcells[-1].b.contents[0]
                    scores[group_name] = score

                groups[class_level] = class_groups

            # create Competition class object
            competition = Competition(comp_name[0], date, scores, recaps, all_groups)
            comp_json = {
                "title": competition.title,
                "date": competition.date,
                "scores": competition.scores,
                "recap": competition.recap,
                "groups": [group.name for group in competition.groups]
            }
            if comp_json not in comps_to_write: # check if competition in list; add if not
                comps_to_write.append(comp_json)
    write_json("./data/competitions.json", comps_to_write, add=True) # write to file
    write_json("./data/groups.json", groups_to_write, add=True) # write to file





if __name__ == '__main__':
    # Configure logger: set format and default level
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=logging.DEBUG
    )

    # Create logger
    logger = logging.getLogger()

    # Create logger filename and path
    LOGPATH = "./wgi_score_parser_log.log"

    # Add logger file and stream handlers
    logger.addHandler(logging.FileHandler(LOGPATH)) # write log to file
    logger.addHandler(logging.StreamHandler(sys.stdout)) # stream log to stdout

    # Start logger
    start_date_time = dt.datetime.now()
    # logger.info(f"Start run: {start_date_time.isoformat()}")
    logger.info("Start run: %s", start_date_time.isoformat()) # log start time



    # links = read_json(URLS)
    # for link in links:
    #     get_competitions(link)
    #     # print(link)

    TEST = 'https://wgi.org/percussion/2019-perc-scores/'
    get_competitions(TEST)




    logger.info("End run: %s", dt.datetime.now().isoformat()) # log end time
