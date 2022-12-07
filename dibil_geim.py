#!/usr/bin/python


import curses


class Map():
    def __init__(self, size):
        self.size = size

    def draw(self):
        pass


class Entity:
    def __init__(self, location):
        self.location = location

    def move(self, location):
        self.location = location

    def draw(self, scr):
        pass


class Player(Entity):
    def __init__(self, location):
        super().__init__(location)


class App():
    def __init__(self, scr):
        self.scr = scr
        init_pairs()

    def run(self):
        while True:
            pass

    def draw(self):
        pass


def color_pair_rgb(self, r, g, b):
    return curses.color_pair(16 + 36*r + 6*g + b)

def init_pairs(self):
    for c in range(256):
        if c != 0: curses.init_pair(c, c, 0)


def main(stdscr):
    app = App(stdscr)
    app.run()


if __name__ == '__main__':
    curses.wrapper(main)
