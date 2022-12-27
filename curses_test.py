#!/usr/bin/python


import curses


def color_pair_rgb(r, g, b):
    return curses.color_pair(16 + 36*r + 6*g + b)


def init_pairs():
    for c in range(1, 7):
        curses.init_pair(c, c, 0)


def main(stdscr):
    init_pairs()
    curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)

    for r in range(6):
        for g in range(6):
            for b in range(6):
                stdscr.addstr(b, 6*r + g, ']', color_pair_rgb(r, g, b) | curses.A_REVERSE)
    
    x, y = 0, 0
    button1_pressed = False
    while True:
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None
        if key == 'KEY_MOUSE':
            _, x, y, _, bstate = curses.getmouse()
            #stdscr.addstr(str(bstate) + ' ')
            if bstate == curses.BUTTON1_PRESSED:
                button1_pressed = True
            elif bstate == curses.BUTTON1_RELEASED:
                button1_pressed = False
            if button1_pressed == True:
                stdscr.addstr(y, x, '[]')
        stdscr.refresh()



if __name__ == '__main__':
    curses.wrapper(main)
