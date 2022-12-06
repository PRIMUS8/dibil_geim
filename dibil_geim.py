#!/usr/bin/python

import curses


class Block():
    def __init__(self, color):
        self.color = colot


class Stone(Block):
    def __init__(self):
        super().__init__()


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

    def run(self):
        while True:
            pass

    def draw(self):
        pass


def main(stdscr):
    app = App(stdscr)
    app.run()


if __name__ == '__main__':
    curses.wrapper(main)
