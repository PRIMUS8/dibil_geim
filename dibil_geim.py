#!/usr/bin/python


import curses, sys, os


#ИГРА:

#Сущности:

pass


#Игра:

pass


#ИГРОВОЕ МЕНЮ:

#Виджеты:

class Widget:
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, texture):
        self.scr = scr
        self.rltv_pos = rltv_pos
        self.dpos_pix = dpos_pix
        self.size_pix = size_pix
        self.texture = texture

    def draw(self):
        render_texture(self.scr, self.get_pos(), self.texture[0])

    def get_pos(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rltv_pos[0]) + self.dpos_pix[0],
                int(scr_size[1] * self.rltv_pos[1]) + self.dpos_pix[1])


class FunctionalWidget(Widget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, texture):
        super().__init__(scr, rltv_pos, dpos_pix, size_pix, texture)

    def handler(self, event):
        pass


class Button(FunctionalWidget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, texture):
        super().__init__(scr, rltv_pos, dpos_pix, size_pix, texture)

    def handler(self, event):
        pass


class TestFuncWidget(FunctionalWidget): #удалить
    def __init__(self, scr):
        super().__init__(scr, (0.5, 0.5), (-4, -4), (8, 8), load_texture('./ascii_textures/example'))


#Страницы меню:

class Page:
    def __init__(self, scr, widgets, basepages, subpages):
        self.scr = scr
        self.widgets = widgets
        self.subpages = subpages
        self.basepages = basepages

    def run(self):
        while True:
            self.draw()
            self.handler()

    def draw(self):
        self.scr.clear()
        for widget in self.widgets:
            widget.draw()
        self.scr.refresh()

    def handler(self):
        try:
            event = self.scr.getkey()
        except:
            event = None
        for widget in self.widgets:
            if isinstance(widget, FunctionalWidget):
                widget.handler(event)


class GameConfigMenu(Page):
    def __init__(self, scr, basepages):
        widgets = []
        subpages = []
        super().__init__(scr, widgets, basepages, subpages)


class SettingsMenu(Page):
    def __init__(self, scr, basepages):
        widgets = []
        subpages = []
        super().__init__(scr, widgets, basepages, subpages)


class MainMenu(Page):
    def __init__(self, scr):
        widgets = [TestFuncWidget(scr)]
        subpages = [GameConfigMenu(scr, [self, self]),
                    SettingsMenu(scr, [self, self])]
        super().__init__(scr, widgets, [self, self], subpages)


#ПРИЛОЖЕНИЕ:

class App:
    def __init__(self):
        sys.stderr = open('./.errbuff', 'a')
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        curses.mousemask(-1)
        curses.start_color()
        curses.curs_set(False)
        self.scr.nodelay(True)
        curses.halfdelay(1)
        init_pairs()

        self.menu = MainMenu(self.scr)

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        self.scr.keypad(False)
        self.scr.nodelay(False)
        curses.endwin()
        sys.stderr = sys.__stderr__
        sys.stderr.write(open('./.errbuff', 'r').read())
        os.remove('./.errbuff')

    def run(self):
        self.menu.run()


#ФУНКЦИИ:

#Цвета:

def color_pair_rgb(r, g, b):
    return curses.color_pair(16 + 36*r + 6*g + b)


def init_pairs():
    for c in range(256):
        if c != 0: curses.init_pair(c, c, 0)


#Текстуры:

def load_texture(path):
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
            if ch != ' ' and r >= 0 and c >= 0 and r < scr_size[0] and c < scr_size[1]:
                scr.addch(r, c, ch)


#ЗАПУСК:

def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
