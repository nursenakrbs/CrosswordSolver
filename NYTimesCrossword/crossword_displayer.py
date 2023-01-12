from tkinter import *
import json
from datetime import date, datetime
import crossword_scraper

clues_across = []
clues_down = []
board = []


def get_today():
    print("\nGetting today's puzzle...")
    crossword_scraper.scrape()
    today = date.today()
    json_path = "puzzles/"
    json_name = "nytimes_puzzle_{}.json".format(today)
    with open(json_path + json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for c in data['clues']:
            if c['orientation'] == "ACROSS":
                clues_across.append(c)

            if c['orientation'] == "DOWN":
                clues_down.append(c)

        for b in data['board']:
            board.append(b)

    display()


def upload_puzzle():
    json_path = "puzzles/"
    json_name = input("\nEnter the name of the puzzle file: ")
    print("\nUploading puzzle...")
    with open(json_path + json_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for c in data['clues']:
            if c['orientation'] == "ACROSS":
                clues_across.append(c)

            if c['orientation'] == "DOWN":
                clues_down.append(c)

        for b in data['board']:
            board.append(b)

    display()


def display():
    print("\nDisplaying the puzzle...")
    main = Tk()
    main.title("NY Times Crossword Puzzle by Nemesis")
    main.config(bg='#FFFFFF')
    photo = PhotoImage(file='crossword-puzzle.png')
    main.iconphoto(False, photo)
    left = Frame(main, width=700, height=700, background='white', borderwidth=0, highlightthickness=0)
    right = Frame(main, width=700, height=700, background='white', borderwidth=0, highlightthickness=0)
    left.pack(side=LEFT)
    right.pack(side=LEFT)

    board_canvas = Canvas(left, width=605, height=505, background='white', bd=0, highlightthickness=0)

    now = datetime.now()
    formatted_now = now.strftime("%B %d, %Y  %H:%M NEMESIS")
    bottom_label_frame = Frame(left, width=50, height=50, background='white', pady=10)
    bottom_label = Label(bottom_label_frame, text=formatted_now, background='white', font="franklin 14 bold")
    bottom_label.pack(side=RIGHT, anchor=E)
    bottom_label_frame.pack(anchor=E, side=BOTTOM)

    width = int((board[0]['width']).replace("px", ""))
    height = int((board[0]['height']).replace("px", ""))

    for b in board:
        y0 = width * (b['coordinate']['x'] - 1)
        x0 = height * b['coordinate']['y']
        x1 = x0 + width
        y1 = y0 + height
        board_canvas.create_line(x0, y0, x0, y1, fill="light grey")
        board_canvas.create_line(x0, y0, x1, y0, fill="light grey")
        if b['fill'] == "rgb(0, 0, 0)":
            board_canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='grey')
        else:
            rect = board_canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='grey')
            if b['label']:
                board_canvas.create_text(x0 + 15, y0 + 15, text=b['label'], fill='black', font='arial 20 bold')
            if b['answer']:
                board_canvas.create_text(x0 + width / 2, y0 + height / 2 + 20, text=b['answer'], fill='blue',
                                         font='arial 50')

    board_canvas.pack(side=RIGHT)

    clues_frame = Frame(right, width=700, height=700, background='white')

    clues_across_frame = Frame(clues_frame, width=300, height=300, background='white', padx=50)
    label_across_frame = Frame(clues_frame, width=50, height=50, background='white', pady=10, padx=50)
    across_text_area = Text(clues_across_frame, width=100, height=15, background='white', bd=0, highlightthickness=0)
    across_label = Label(label_across_frame, text='ACROSS', background='white', font="franklin 14 bold")

    label_across_frame.pack(anchor=W)
    clues_across_frame.pack(side=TOP)
    across_label.pack(side=LEFT)
    across_text_area.pack(fill=BOTH)

    clues_down_frame = Frame(clues_frame, width=300, height=300, background='white', padx=50)
    label_down_frame = Frame(clues_frame, width=50, height=50, background='white', pady=10, padx=50)
    down_text_area = Text(clues_down_frame, width=100, height=15, background='white', bd=0, highlightthickness=0)
    down_label = Label(label_down_frame, text='DOWN', background='white', font="franklin 14 bold")

    label_down_frame.pack(anchor=W)
    clues_down_frame.pack(side=TOP)
    down_label.pack(side=LEFT)
    down_text_area.pack(fill=BOTH)

    line_ind = 0
    label_end = 0
    char_ind = 0
    for clue in clues_across:
        label_end = 0
        char_ind = 0
        text = clue['label'] + "\t" + clue['clue'] + "\n"
        across_text_area.insert(END, text)
        for c in text:
            if c == "\t":
                break
            label_end += 1

        char_ind = label_end + 1
        line_ind += 1

        label_tag_start = str(line_ind) + ".0"
        label_tag_end = str(line_ind) + "." + str(char_ind)
        across_text_area.tag_add("label", label_tag_start, label_tag_end)

        clue_tag_start = str(line_ind) + "." + str(char_ind)
        clue_tag_end = str(line_ind) + "." + str(len(clue['label'] + " " + clue['clue']))
        across_text_area.tag_add("clue", clue_tag_start, clue_tag_end)
        across_text_area.tag_config("label", font="franklin 14 bold")
        across_text_area.tag_config("clue", font="franklin 12")

    line_ind = 0
    label_end = 0
    char_ind = 0
    for clue in clues_down:
        label_end = 0
        char_ind = 0
        text = clue['label'] + "\t" + clue['clue'] + "\n"
        down_text_area.insert(END, text)
        for c in text:
            if c == "\t":
                break
            label_end += 1

        char_ind = label_end + 1
        line_ind += 1

        label_tag_start = str(line_ind) + ".0"
        label_tag_end = str(line_ind) + "." + str(char_ind)
        down_text_area.tag_add("label", label_tag_start, label_tag_end)

        clue_tag_start = str(line_ind) + "." + str(char_ind)
        clue_tag_end = str(line_ind) + "." + str(len(clue['label'] + " " + clue['clue']))
        down_text_area.tag_add("clue", clue_tag_start, clue_tag_end)
        down_text_area.tag_config("label", font="franklin 14 bold")
        down_text_area.tag_config("clue", font="franklin 12")

    clues_frame.pack()
    main.mainloop()


if __name__ == '__main__':

    print("Welcome to NY Times Crossword Puzzle!")
    print("What do you want to do?")
    print("1. Get today's puzzle")
    print("2. Upload past puzzle")

    option = input("Enter option number: ")

    if option == "1":
        get_today()
    elif option == "2":
        upload_puzzle()
    else:
        print("\nUnknown option. Exiting...")
