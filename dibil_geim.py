#!/usr/bin/python


import curses


#ИГРА:

#Сущности:

pass


#Игра:

pass


#ИГРОВОЕ МЕНЮ:

#Виджеты:

class Wiget():
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, texture):
        self.scr = scr
        self.rltv_pos = rltv_pos
        self.dpos_pix = dpos_pix
        self.size_pix = size_pix
        self.texture = texture

    def draw(self):
        render_texture(self.scr, self.get_pos(), texture[0])

    def get_pos(self):
        scr_size = scr.getmaxyx()
        return scr_size[0] * rltv_pos[0] + dpos_pix[0], scr_size[1] * rltv_pos[1] + dpos_pix[1]


class FunctionalWiget(Wiget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix texture):
        super().__init__(scr, rltv_pos, dpos_pix, size_pix, texture)

    def handler():
        pass


class Button(FunctionalWiget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix):
        super().__init__(scr, rltv_pos, dpos_pix, size_pix)


class TestFuncWiget(FunctionalWiget): #удалить
    def __init__(self, scr):
        super().__init__(scr, (0.5, 0.5), (-4, -4), (8, 8))

    def draw(self):
        pass


#Страницы меню:

class Page():
    def __init__(self, scr, wigets, pasepages, subpages):
        self.scr = scr
        self.wigets = wigets
        self.subpages = subpages
        self.basepages = basepages

    def run(self):
        while True:
            self.draw()
            self.handler()

    def draw(self):
        for wiget in self.wigets:
            wiget.draw

    def handler(self):
        for wiget in wigets:
            if isinstance(wiget, FunctuonalWiget):
                wiget.handler()


class Game_config_menu(Page):
    def __init__(self, scr, root, back):
        wigets = []
        subpages = []
        super().__init__(scr, wigets, [root, back], subpages)


class Settings_menu(Page):
    def __init__(self, scr, root, back):
        wigets = []
        subpages = []
        super().__init__(scr, wigets, [root, back], subpages)


class Main_menu(Page):
    def __init__(self, scr):
        wigets = []
        subpages = [Game_config_menu(scr, self, self),
                    Settings_menu(scr, self, self)]
        super().__init__(scr, wigets, subpages)


#ПРИЛОЖЕНИЕ:

class App():
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.mousemask(-1)
        curses.start_color()
        curses.curs_set(False)
        init_pairs()
        self.menu = Main_Menu(self.scr)

    def __del__(self):
        curses.echo()
        surses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def run(self):
        self.menu.run()


#ДОП. ФУНКЦИИ:

#Цвета:

def color_pair_rgb(self, r, g, b):
    return curses.color_pair(16 + 36*r + 6*g + b)


def init_pairs(self):
    for c in range(256):
        if c != 0: curses.init_pair(c, c, 0)


#Текстуры:

def unpack_texture(path):
    texture = open(path, 'r').read()
    texture = texture.split('\n')
    shape = [int(i) for i in texture.pop(0).split('x')]
    texture = [texture[i:i+shape[1]] for i in range(0, shape[2]*shape[1], shape[1])]
    return texture


def render_texture(scr, pos, texture):
    scr_size = scr.getmaxyx()
    for ri, st in enumerate(texture):
        for ci, ch in enumerate(st):
            r = pos[0] + ri
            c = pos[1] + ci
            if ch != ' ' and r >= 0 and c >= 0 and r <= scr_size[0] and c <= scr_size[1]:
                scr.addch(r, c, ch)


#ЗАПУСК:

def main(stdscr):
    app = App()
    app.run()


if __name__ == '__main__':
    main()
