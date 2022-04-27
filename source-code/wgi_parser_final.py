"""
This program/module parses scores from https://wgi.org for the scores from each
competition. Writes each Competition to competitions.json and each Group
to groups.json.
"""
from dataclasses import dataclass
import json
import logging
import os
import re
import sys
import datetime as dt
import requests
from bs4 import BeautifulSoup as bs

URLS = "./urls.json"
CACHE = {}
CACHE_PATH = './cache/cache.json'

# Classes

@dataclass()
class Group:
    """creates a group class object"""
    name: str
    class_level: str
    location: str
    competitions: dict

    def jsonify(self):
        """returns class object as json"""
        group_json = {
            "name": self.name,
            "class_level": self.class_level,
            "location": self.location,
            "competitions": self.competitions
        }
        return group_json

@dataclass()
class Competition:
    """creates a competition class object"""
    title: str
    date: str
    scores: str
    recap: str
    groups: list
    scores_by_group: dict

    def jsonify(self):
        """returns class object as json"""
        comp_json = {
            "title": self.title,
            "date": self.date,
            "scores": self.scores,
            "recap": self.recap,
            "groups": [group.name for group in self.groups],
            "scores_by_group": self.scores_by_group
        }
        return comp_json





# Functions
def read_json(filepath:str, encoding='utf-8') -> dict:
    """Reads a json file and returns a dictionary of the object
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def write_json(filepath:str, data, encoding='utf-8', ensure_ascii=False, indent=4):
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

    Returns:
        None
    """
    if not os.path.exists(filepath):
        with open(filepath, 'a', encoding=encoding) as file_obj:
            json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
    else:
        with open(filepath, 'w', encoding=encoding) as file_obj:
            json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def get_content(url:str) -> str:
    """Takes a url and returns the html content

    params:
        url(string): link to html content

    returns:
        response.text: html content
    """
    response = requests.get(url)
    logger.info("Fetching content from %s...", url)

    return response.text

def read_cache() -> dict:
    """ reads the cache file
        returns the cache
    """
    cache = read_json(CACHE_PATH)
    logger.info("Reading from cache...")
    return cache


def check_cache(url:str) -> str:
    """ checks cache for url.
        if url not in cache, adds it and rewrites the cache.
        returns html content
    """
    cache = read_cache()
    if url not in cache.keys():
        cache[url] = get_content(url)
        write_json(CACHE_PATH, cache)
        logger.info("Writing %s to cache...", url)
    logger.info("Fetching %s from cache...", url)
    return cache[url]


def get_competitions(url):
    """gets competition data
    """
    html_data = check_cache(url)

    soup = bs(html_data, 'html.parser')
    logger.info("Parsing page: %s", url)

    table_rows = soup.find_all('tr') # list of table rows

    comps = []

    for t_r in table_rows[:-1]:
        tr_children = [child for child in t_r.children] # find children
        if len(tr_children) == 3: # rows with dates
            year = re.search("20..", url).group()
            date = f"{tr_children[1:-1:1][0].strong.contents[0]}, {year}" # month day, year
        elif len(tr_children) == 9: # rows with groups and scores
            tr_children_data = tr_children[1::2][1:]
            comp_name = tr_children_data[0].contents[0] # get competition name # list

            # check if there is a link to scores # some don't have scores
            if tr_children_data[1].a:
                scores = tr_children_data[1].a['href'] # get link to scores
            else:
                scores = "No scores"
                logger.info("No scores found for %s", comp_name)

            # check if there is a link to recaps # some don't have recaps
            if tr_children_data[-1].a:
                recaps = tr_children_data[-1].a['href'] # get link to recaps
            else:
                recaps = "No recaps"
                logger.info("No recaps found for %s", comp_name)

            # create Competition obj with placeholder for scores_by_group
            comp_data = Competition(comp_name, date, scores, recaps, [], {})
            comps.append(comp_data)
    return comps







def get_groups_scores(comp_obj:Competition) -> tuple:
    """ parses page with scores.
        Returns a tuple that contains a list of Groups and a dictionary of scores_by_group
    """
    scores_page = comp_obj.scores # url for scores page
    if "https://" not in comp_obj.scores : # == "No scores"
        scores_by_group = {"No groups participated in this competition": "No scores to report"}
    else:
        html_data = check_cache(scores_page)

        soup = bs(html_data, 'html.parser')
        logger.info("Parsing page: %s", scores_page)

        groups_list = [] # list of Group objects
        scores_by_group = {}

        scores_div = soup.find_all('div', attrs={'class': 'table-responsive'}) # list of divs
        scores_table = scores_div[0].table
        table_rows = scores_table.find_all('tr')

        for row in table_rows:
            tcells = list(row.children)
            if len(tcells) == 3: # rows with class levels
                class_level = tcells[1].b.contents[0] # group class_level
            elif len(tcells) == 4: # rows with group names
                em = tcells[2].contents[1]
                group_name = tcells[2].contents[0].strip() # group names
                location = em.contents[0].replace('(', '').replace(')', '') # group location

                score = tcells[-1].b.contents[0]

                group_data = Group(group_name, class_level, location, [])
                groups_list.append(group_data)

                scores_by_group[group_data.name] = score

        return groups_list, scores_by_group





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


    all_competitions = [] # store competition objects
    all_groups = [] # store group objects

    comps_to_write = [] # competitions to write
    groups_to_write = [] # groups to write


    for link in read_json(URLS):
        # check_cache(link)
        # get_competitions
        competitions = get_competitions(link)

        # get groups and score data for each competition
        for comp in competitions:
            groups_and_scores = get_groups_scores(comp)

            if isinstance(groups_and_scores, tuple):
                groups, scores = groups_and_scores
                comp.groups = groups # update Competition class obj with groups list
                comp.scores_by_group = scores # update Competition class obj with scores dict

                if len(groups) > 1:
                    for group in groups:
                        all_groups.append(group)

            all_competitions.append(comp)

            comps_to_write.append(comp.jsonify())




    for group in all_groups:
        # dict of comps and scores
        group_comps = {}
        for comp in all_competitions:
            if group in comp.groups:
                group_comps[f"{comp.title}, {comp.date}"] = comp.scores_by_group.get(group.name) # get score for that group
        group.competitions = group_comps

        groups_to_write.append(group.jsonify())


    # TODO combine duplicate groups -> combine competitions dicts
    # TODO check for duplicate comps
    # TODO normalize location names

    # sort groups by name, class_level
    groups_to_clean = sorted(groups_to_write, key=lambda x: (x['name'], x['class_level']))
    clean_groups = []
    done_cleaning = []

    # find duplicate group entries, combine competitions
    for i, group in enumerate(groups_to_clean):
        if len(clean_groups) == 0:
            clean_groups.append(group)
        elif group['name'] == clean_groups[-1]['name'] and group['class_level'] == clean_groups[-1]['class_level']:
            if clean_groups[-1]['competitions'] != group['competitions']:
                clean_groups[-1]['competitions'] |= group['competitions']
                if clean_groups[-1] not in done_cleaning:
                    done_cleaning.append(clean_groups[-1])
        else:
            clean_groups.append(group)
            if clean_groups[-1] not in done_cleaning:
                done_cleaning.append(clean_groups[-1])

    write_json('./data/competitions.json', comps_to_write)
    logger.info("%s Competitions written to file", len(comps_to_write))
    write_json('./data/groups.json', done_cleaning)
    logger.info("%s Groups written to file", len(done_cleaning))


    logger.info("End run: %s", dt.datetime.now().isoformat()) # log end time

