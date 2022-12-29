#!/usr/bin/python


import curses
import os


def color_pair_fb(fb):
    return curses.color_pair((fb[0] + 1)*9 + fb[1] + 1)


def init_pairs_fb():
    for c1 in range(9):
        for c2 in range(9):
            curses.init_pair(c1*9 + c2, c1 - 1, c2 - 1)


def main(stdscr):
    curses.use_default_colors()
    init_pairs_fb()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(0)
    curses.curs_set(False)

    x, y = 0, 0
    color1, color2 = 0, 0
    button1_pressed = False
    while True:
        for c1 in range(9):
            for c2 in range(9):
                stdscr.addstr(c1 + 5, c2 * 2 + 2, '[]', color_pair_fb((c1 - 1, c2 - 1)) | curses.A_BOLD)
                if color1 == c1 and color2 == c2:
                    stdscr.addstr(c1 + 5, c2 * 2 + 2, '>', curses.color_pair(0) | curses.A_BLINK)
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None
        stdscr.addstr(1, 2, key + '..............')
        if key == 'KEY_RIGHT':
            color2 += 1
        elif key == 'KEY_LEFT':
            color2 += -1
        elif key == 'KEY_DOWN':
            color1 += 1
        elif key == 'KEY_UP':
            color1 += -1
        if key == 'KEY_MOUSE':
            _, x, y, _, bstate = curses.getmouse()
            stdscr.addstr(2, 2, str(bstate) + '..............')
            if bstate == curses.BUTTON1_PRESSED:
                button1_pressed = True
            elif bstate == curses.BUTTON1_RELEASED:
                button1_pressed = False
            if button1_pressed == True:
                stdscr.addstr(y, x if x % 2 == 0 else x - 1, '[]', curses.color_pair(color1*9 + color2) | curses.A_BOLD)
        stdscr.refresh()



if __name__ == '__main__':
    os.environ['TERM'] = 'xterm-1003'
    curses.wrapper(main)
