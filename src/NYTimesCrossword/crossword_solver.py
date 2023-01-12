import json
import os
import itertools
from collections import namedtuple
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import enchant

articles = ("a", "an", "the", "of", "at")
d = enchant.Dict("en_US")

# Constants
Clue = namedtuple('Clue', 'no label orient pos desc len ans')
ACROSS = 'across'
DOWN = 'down'
BLOCKED = '-'

# Global Variables
clues = []
board = [[(x, y) for x in range(5)] for y in range(5)]
label_coor = [(0, 0) for x in range(11)]


def read_crossword(json_name):
    with open(json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for b in data['board']:
            # x and y is swapped because of a mistake in the website
            x = b['coordinate']['y'] - 1
            y = b['coordinate']['x'] - 1
            if b['label'] != '':
                label_coor[int(b['label'])] = (x, y)
            if b['answer'] == '':
                board[y][x] = BLOCKED
            else:
                board[y][x] = b['answer']

        clue_index = 0
        for c in data['clues']:
            answer = ''
            orient = ACROSS if c['orientation'] == "ACROSS" else DOWN
            length = 0
            coor = label_coor[int(c['label'])]
            x = coor[0]
            y = coor[1]
            while not (y >= 5 or x >= 5 or board[y][x] == BLOCKED):
                answer += board[y][x]
                length += 1
                x += int(orient == ACROSS)
                y += int(orient == DOWN)
            coor = label_coor[int(c['label'])]
            clues.append(Clue(clue_index, c['label'], orient, coor, c['clue'], length, answer))
            clue_index += 1


def remove_special_characters(in_str):
    s = in_str.replace("___", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    return s


def css_exists(element, css):
    try:
        element.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


def conceptnet(chrome_driver, clue_text, clue):
    chrome_driver.get("http://conceptnet.io/")
    candidate_list = []
    search = chrome_driver.find_element_by_name("text")
    search.send_keys(clue_text)
    search.send_keys(Keys.ENTER)
    h1 = chrome_driver.find_elements_by_css_selector("#main > div.header > div > div.pure-u-2-3 > h1")
    if h1[0].text == "Not found":
        return None
    else:
        if css_exists(chrome_driver, "div.rel-grid > div.pure-g > div > ul > li.more > a"):
            more_links = chrome_driver.find_elements_by_css_selector("div.rel-grid > div.pure-g > div > ul > li.more > a")
            cur_win = chrome_driver.current_window_handle
            for more in more_links:
                more.click()
                chrome_driver.switch_to_window([win for win in chrome_driver.window_handles if win != cur_win])
                start_edges = chrome_driver.find_elements_by_css_selector("table.edge-table > tbody > tr > td.edge-start > span.term.lang-en > a")
                for edge in start_edges:
                    candidate = edge.text
                    for art in articles:
                        if edge.text.startswith(art + " "):
                            candidate = edge.text.replace(art + " ", "")

                    if len(candidate) == int(clue.len):
                        candidate_list.append(candidate)

                chrome_driver.close()
                chrome_driver.switch_to_window(cur_win)


        # divs = chrome_driver.find_elements_by_css_selector("#main > div.content > div.rel-grid > div > div")
        # for div in divs:
        #     ul = div.find_element_by_css_selector(" > ul")
        #     list_items = ul.find_elements_by_css_selector(" > li")
        #     for item in list_items:
        #         a = item.find_element_by_css_selector("> a")
        #     # for i in range(clue.len):


# main > div.content > div.rel-grid > div > div:nth-child(1) > ul > li:nth-child(1) > a:nth-child(2)


print("\nBoard:")
for b0 in board:
    print(b0)

json_filename = "puzzles/nytimes_puzzle_2020-12-11.json"
read_crossword(json_filename)

print('\nClues:')
for c0 in clues:
    print(c0)

print('\nBoard:')
for b1 in board:
    print(b1)

path = os.path.abspath("chromedriver")
chrome_driver = webdriver.Chrome(executable_path=path)
for clue in clues:
    clue_text = remove_special_characters(clue.desc.lower())
    word_subsets = []
    splitted = clue_text.split()

    for i in range(1, len(splitted)):
        word_subsets += list(itertools.combinations(splitted, i))

    for subset in word_subsets:
        if subset[0] in articles:
            continue
        conceptnet(chrome_driver, subset, clue)
