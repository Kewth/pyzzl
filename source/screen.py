'屏幕及 IO 管理'

import time
import curses

class char:
    '单个字符'
    def __init__(self, text, font = curses.COLOR_WHITE, back = curses.COLOR_BLACK):
        self.font = font
        self.back = back
        self.text = text

stdscr = None
LINE = None
COL = None
pair_lis = [(curses.COLOR_WHITE, curses.COLOR_BLACK)]

def init(scr, line, col):
    '初始化，返回是否成功'

    global stdscr, LINE, COL
    stdscr = scr
    LINE = line
    COL = col
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    if curses.LINES < line or curses.COLS < col:
        return False
    return True

def getch(): # int
    c = stdscr.getch()
    while c == curses.ERR:
        c = stdscr.getch()
    return c

def ifgetch(wait): # int
    clock = time.time()
    c = stdscr.getch()
    while c == curses.ERR and time.time() < clock + wait:
        c = stdscr.getch()
    return c

def choose(lis, free = False): # int
    c = stdscr.getch()
    if free:
        while c == curses.ERR:
            c = stdscr.getch()
        if chr(c) in lis:
            return c
        return curses.ERR
    else:
        while c == curses.ERR or not chr(c) in lis:
            c = stdscr.getch()
    return c

def getstr(x, y, tips):
    write(x, y, tips)
    y += len(tips)
    c = getch()
    s = ''
    while c != curses.KEY_ENTER and c != ord('\n'):
        write(x, y, chr(c))
        y += 1
        s += chr(c)
        c = getch()
    return s

def write(x, y, text):
    stdscr.addstr(x, y, text)

def getpair(font, back):
    for i in range(len(pair_lis)):
        if pair_lis[i][0] == font and pair_lis[i][1] == back:
            return i
    i = len(pair_lis)
    curses.init_pair(i, font, back)
    pair_lis.append((font, back))
    return i

def write_ch(x, y, ch):
    i = getpair(ch.font, ch.back)
    stdscr.addstr(x, y, ch.text, curses.color_pair(i))

def infobox(topic, text_list):
    infobox.topic = topic
    infobox.text_list = text_list
    infobox.clock = time.time()
    # infobox.p1 = 0
    # infobox.p2 = 0

infobox.topic = ''
infobox.text_list = []
infobox.clock = 0
# infobox.p1 = 0
# infobox.p2 = 0

def refresh(show_info = True):
    if show_info:
        # if infobox.p1 < len(infobox.text_list):
        #     if time.time() > infobox.clock + 0.05:
        #         infobox.p2 += 1
        #         if infobox.p2 >= len(infobox.text_list[infobox.p1]):
        #             infobox.p1 += 1
        #             infobox.p2 = 0
        #         infobox.clock += 0.05
        #     for i in range(infobox.p1):
        #         stdscr.addstr(3 + i, 20, infobox.text_list[i])
        #     if infobox.p1 < len(infobox.text_list):
        #         stdscr.addstr(3 + infobox.p1, 20, infobox.text_list[infobox.p1][:infobox.p2 + 1])
        # else:
        #     if time.time() > infobox.clock + 5.0:
        #         infobox.text_list = []
        #         infobox.p1 = 0
        #         infobox.p2 = 0
        #     for i in range(len(infobox.text_list)):
        #         stdscr.addstr(3 + i, 20, infobox.text_list[i])
        if time.time() > infobox.clock + 5.0:
            infobox.topic = ''
            infobox.text_list = []
        pair_i = getpair(curses.COLOR_WHITE, curses.COLOR_BLUE)
        stdscr.addstr(2, 18, infobox.topic, curses.color_pair(pair_i))
        for i in range(len(infobox.text_list)):
            stdscr.addstr(3 + i, 20, infobox.text_list[i])
    stdscr.refresh()

def clear():
    stdscr.clear()
