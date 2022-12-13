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


class Wiget():
    def __init__(self, scr):
        self.scr = scr

    def draw(self):
        pass

    def get_event(self):
        return None


class Button(Wiget):
    def  __init__(self, scr):
        super().__init__(scr)


class Menu():
    def __init__(self, scr):
        self.scr = scr
        self.wigets = []

    def run(self):
        while True:
            self.draw()
            event = self.get_event()
            if event != None()
                return event

    def draw(self):
        for wiget in self.wigets:
            wiget.draw()

    def get_event(self):
        for wiget in self.wigets:
            event = wiget.get_event()
            if event != None:
                return event
        return None:


class Game():
    def __init__(self, scr):
        self.scr = scr

    def run(self):
        while True:
            self.draw()

    def draw(self):
        pass


class App():
    def __init__(self, scr):
        self.scr = scr
        init_pairs()
        self.menu = Menu(self.scr)
        self.game = Game(self.scr)

    def run(self):
        while True()
            if self.menu.run() == 'start':
                self.game.run()
            else:
                break


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
