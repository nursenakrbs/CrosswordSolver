import json

board = []
clues = []
across_solutions = []
down_solutions = []


def read_crossword():
    json_name = "puzzles/nytimes_puzzle_2020-12-10.json"
    with open(json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for cell in data['board']:
            x = cell['coordinate']['x'] - 1
            y = cell['coordinate']['y'] - 1
            board[x][y] = {
                "label": cell['label'],
                "fill": cell['fill'],
                "letter": cell['answer']
            }


def customize():
    for row in range(5):
        for col in range(5):
            if board[row][col]['fill'] == "rgb(0, 0, 0)":
                continue

            if row == 0:
                down_solutions[col] = {
                    'length': 1,
                    'answer': board[row][col]['letter'],
                    'label': board[row][col]['label']
                }
                board[row][col]['down_clue'] = {
                    'clue_no': board[row][col]['label'],
                    'ch_count': 1
                }
            else:
                if board[row - 1][col]['letter'] != '':
                    down_solutions[col] = {
                        'length': down_solutions[col]['length'] + 1,
                        'answer': down_solutions[col]['answer'] + board[row][col]['letter'],
                        'label': down_solutions[col]['label']
                    }
                    board[row][col]['down_clue'] = {
                        'clue_no': board[row - 1][col]['clue_no'],
                        'ch_count': board[row - 1][col]['clue_no'] + 1
                    }
                else:
                    down_solutions[col] = {
                        'length': 1,
                        'answer': board[row][col]['letter'],
                        'label': board[row][col]['label']
                    }
                    board[row][col]['down_clue'] = {
                        'clue_no': board[row][col]['label'],
                        'ch_count': 1
                    }

            if col == 0:
                across_solutions[row] = {
                    'length': 1,
                    'answer': board[row][col]['letter'],
                    'label': board[row][col]['label']
                }
                board[row][col]['across_clue'] = {
                    'clue_no': board[row][col]['label'],
                    'ch_count': 1
                }
            else:
                if board[row][col - 1]['across_clue']['letter'] != '':
                    across_solutions[row] = {
                        'length': across_solutions[row]['length'] + 1,
                        'answer': across_solutions[col]['answer'] + board[row][col]['letter'],
                        'label': across_solutions[col]['label']
                    }
                    board[row][col]['across_clue'] = {
                        'clue_no': board[row][col - 1]['clue_no'],
                        'ch_count': board[row][col - 1]['clue_no'] + 1
                    }
                else:
                    across_solutions[row] = {
                        'length': 1,
                        'answer': board[row][col]['letter'],
                        'label': board[row][col]['label']
                    }
                    board[row][col]['across_clue'] = {
                        'clue_no': board[row][col]['label'],
                        'ch_count': 1
                    }
