#!/usr/bin/python


import curses


class Map():
    def __init__(self, size):
        self.size = size

    def draw(self):
        pass


class Entity:
    def __init__(self, pos):
        self.location = pos

    def move(self, pos):
        self.pos = pos

    def draw(self, scr):
        pass


class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos)


class Game():
    def __init__(self, scr):
        self.scr = scr

    def run(self):
        while True:
            self.draw()

    def draw(self):
        pass


class Wiget():
    def __init__(self, scr, pos_proc, dpos_pix, size_pix):
        self.scr = scr
        self.pos_proc = pos_proc
        self.dpos_pix = dpos_pix
        self.size_pix = size_pix

    def draw(self):
        pass

    def get_event(self):
        return None


class Button(Wiget):
    def  __init__(self, scr, pos_proc, dpos_pix, size_pix):
        super().__init__(scr, pos_proc, dpos_pix, size_pix)


class Page():
    def __init__(self, scr, wigets, subpages):
        self.scr = scr
        self.wigets = wigets
        self.subpages = subpages

    def run(self):
        while True:
            self.draw()
            self.event_handler()

    def draw(self):
        for wiget in self.wigets:
            wiget.draw

    def event_handler(self):
        pass


class Main_menu(Page):
    def __init__(self, scr):
        wigets = []
        subpages = []
        super().__init__(scr, wigets, subpages)

    def event_handler(self):
        pass


class App():
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.mousemask(-1)
        curses.start_color()
        init_pairs()
        self.menu = Main_Menu(self.scr)

    def __del__(self):
        curses.echo()
        surses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def run(self):
        self.menu.run()


def color_pair_rgb(self, r, g, b):
    return curses.color_pair(16 + 36*r + 6*g + b)

def init_pairs(self):
    for c in range(256):
        if c != 0: curses.init_pair(c, c, 0)


def main(stdscr):
    app = App()
    app.run()


if __name__ == '__main__':
    main()
