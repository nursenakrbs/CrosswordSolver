import json
import os
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

Clue = namedtuple('Clue', 'no label orient pos desc len ans')
ACROSS = 'across'
DOWN = 'down'
BLOCKED = '-'

clues = []
words = [None for x in range(11)]
board = [[(x, y) for x in range(5)] for y in range(5)]
ind_board = [[[] for x in range(5)] for y in range(5)]  # for storing clue letter indexes
label_coor = [(0, 0) for x in range(11)]


def score():  # lower is better
	res = 0
	for by in ind_board:
		for b in by:
			if len(b) == 2:
				l1 = words[b[0][0]][b[0][1]]
				l2 = words[b[1][0]][b[1][1]]
				# print( words[b[0][0]], " ", b[0][1] )
				# print( words[b[1][0]], " ", b[1][1] )
				# print( "l1: ", l1, "l2: ", l2 )
				res += int(l1 != l2)  # if letters aren't matching
	return res


print("\nBoard:")
for b in board:
	print(b)

json_name = "puzzles/nytimes_puzzle_2020-12-11.json"
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
			ind_board[y][x].append((clue_index, length))
			answer += board[y][x]
			length += 1
			x += int(orient == ACROSS)
			y += int(orient == DOWN)
		coor = label_coor[int(c['label'])]
		clues.append(Clue(clue_index, c['label'], orient, coor, c['clue'], length, answer))
		clue_index += 1
	for i in range(clue_index):
		words[i] = clues[i].ans

print('\nClues:')
for c in clues:
	print(c)

print('\nBoard:')
for b in board:
	print(b)

print('\nWord index Board:')
for b in ind_board:
	print(b)


print("\nScore (lower is better): ", score())
words[0] = 'four'
print('Intentionally changed a word')
print("Score: ", score())


