from bs4 import BeautifulSoup as bs
import requests
import random
import logging
import numpy as np
import validation as v
from urllib.parse import urljoin

def clean_url(url: str) -> str:
    return url.replace('(','').replace(')','').lower().strip()

def nlp_solve(start_page: str, target_page: str, 
          model_words: dict, model_vecs: list):
    """
    Traverse wikipedia selecting pages based on a similarity score relative to your target page. 
    If the target page is found, return True. 
    Otherwise continue scoring and picking links until it is found.
    Keeps track of visited pages to avoid re-visiting. If there is a dead end (no accessible links),
    it will re-direct to Special:Random to fix the issue.
    Testing based on word2vec NLP model trained with english wikipedia text
    """
    visited = {}
    if not v.valid_url(start_page, visited):
        logging.info("Provided start page is not compatible with the wiki game.")
    if not v.valid_url(target_page, visited):
        logging.info("Provided target page is not compatible with the wiki game.")
    
    base = "https://en.wikipedia.org/wiki/"
    valid_target_indices = []
    target_words = clean_url(target_page).split(base)[1].split("_")

    for target_word in target_words:
        if target_word in model_words:
            i = model_words[target_word]
            logging.info("found " + target_word + 
                         " in model at index " + str(i))
            valid_target_indices.append(i)
    
    if len(valid_target_indices) == 0:
        logging.info("Unfortunately, your target page was not compatible with the NLP model "
                          "most likely due to the obscurity of the words.")
        return
    
    current_response = requests.get(start_page)
    soup = bs(current_response.text, "html.parser")

    visited[start_page] = True

    found = start_page == target_page
    if found:
        logging.info("Start and target were the same page.")
        return
    
    logging.info("Starting traversal -----")
    logging.info("Start page: %s" % start_page)
    logging.info("Target page: %s" % target_page)

    iter = 0
    while not found:
        links = {}
        for link in soup.find_all("a"):
            url = urljoin(base, link.get("href", ""))
            if v.valid_url(url, visited):
                links[url] = clean_url(link.text)

        if target_page in links:
            found = True
            logging.info("Success! Found your target page in %i steps" % iter)
        else:
            if len(links) > 0:
                best_score = 0
                best_link = list(links.keys())[0]
                for link in links:
                    val = links[link]
                    lookups = val.split("_")
                    score, failed_lookups = 0, 0
                    for lookup in lookups:
                        for valid_index in valid_target_indices:
                            if lookup in model_words:
                                lookup_index = model_words[lookup]
                                vec1 = model_vecs[lookup_index, :]
                                vec2 = model_vecs[valid_index, :]
                                score += (np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
                            else:
                                failed_lookups += 1
                    total_lookups = len(lookups) - failed_lookups
                    if total_lookups == 0 or len(valid_target_indices) == 0:
                        avg_score = 0
                    else:
                        avg_score = (score / (total_lookups*len(valid_target_indices)))
                    if avg_score > best_score:
                        best_score = avg_score
                        best_link = link
            else:
                logging.info("You've reached a dead end. Picking a random wiki link to re-route.")
                best_link = "https://en.wikipedia.org/wiki/Special:Random"

            logging.info(best_link)
            visited[best_link] = True
            current_response = requests.get(best_link)
            soup = bs(current_response.text, "html.parser")
            iter += 1

def random_solve(start_page: str, target_page: str):
    """
    Traverse wikipedia selecting random pages linked from your start page. 
    If the target page is found, return True. 
    Otherwise continue picking random links until it is found.
    Keeps track of visited pages to avoid re-visiting. If there is a dead end (no accessible links),
    it will re-direct to Special:Random to fix the issue.
    """
    visited = {}
    if not v.valid_url(start_page, visited):
        logging.info("Provided start page is not compatible with the wiki game.")
    if not v.valid_url(target_page, visited):
        logging.info("Provided target page is not compatible with the wiki game.")

    base = "https://en.wikipedia.org/wiki/"

    current_response = requests.get(start_page)
    soup = bs(current_response.text, "html.parser")
    
    visited[start_page] = True

    found = start_page == target_page
    if found:
        logging.info("Start and target were the same page.")
        return
    
    logging.info("Starting traversal -----")
    logging.info("Start page: %s" % start_page)
    logging.info("Target page: %s" % target_page)

    iter = 0
    while not found:
        links = {}
        for link in soup.find_all("a"):
            url = urljoin(base, link.get("href", ""))
            if v.valid_url(url, visited):
                links[url] = clean_url(link.text)
        if target_page in links:
            found = True
            logging.info("Success! Found your target link in %i steps." % iter)
        else:
            if len(links) > 0:
                random_link = random.choice(list(links.keys()))
            else:
                logging.info("You've reached a dead end. Picking a random wiki link to re-route.")
                random_link = "https://en.wikipedia.org/wiki/Special:Random"
            logging.info(random_link)
            visited[random_link] = True
            current_response = requests.get(random_link)
            soup = bs(current_response.text, "html.parser")
            iter += 1
