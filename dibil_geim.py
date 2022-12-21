#!/usr/bin/python


import curses, sys, os


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
        pass


class SubApp:
    def __init__(self, scr):
        self.scr = scr

    def handle(self):
        pass


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
    def __init__(self, scr, widgets, subpages):
        self.scr = scr
        self.widgets = widgets
        self.subpages = subpages

    def draw(self):
        self.scr.clear()
        for widget in self.widgets:
            widget.draw()
        self.scr.refresh()

    def handler(self):
        try:
            event = self.scr.getkey()
        except curses.error:
            event = None
        for widget in self.widgets:
            if isinstance(widget, FunctionalWidget):
                widget.handler(event)
        self.draw()


class GameConfig(Page):
    def __init__(self, scr):
        widgets = []
        subpages = []
        super().__init__(scr, widgets, subpages)


class Settings(Page):
    def __init__(self, scr):
        widgets = []
        subpages = []
        super().__init__(scr, widgets, subpages)


class MainPage(Page):
    def __init__(self, scr):
        widgets = [TestFuncWidget(scr)]
        subpages = [self,
                    GameConfigMenu(scr),
                    SettingsMenu(scr)]
        super().__init__(scr, widgets,  subpages)

class Menu(SubApp):
    def __init__(self, scr):
        super().__init__(scr)
        self.pages = []



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
    buffer = texture
    texture = []
    for fri in range(shape[3]):
        fr = []
        for sti in range(shape[2]):
            st = []
            for cri in range(shape[1]):
                cr = []
                for cni in range(shape[0]):
                    cn = buffer[fri*shape[2] + sti][cni*shape[1] + cri]
                    if cni == 0:
                        cr.append(cn)
                    else:
                        cr.append(int(cn))
                st.append(cr)
            fr.append(st)
        texture.append(fr)
    return texture


def render_texture_rgba(scr, pos, texture):
    scr_size = scr.getmaxyx()
    for ri, st in enumerate(texture):
        for ci, cr in enumerate(st):
            r = pos[0] + ri
            c = pos[1] + ci
            if cr[4] > 0 and r >= 0 and c >= 0 and r < scr_size[0] and c < scr_size[1]:
                scr.addch(r, c, cr[0], color_pair_rgb(cr[1], cr[2], cr[3]))


def render_texture_rgb(scr, pos, texture):
    scr_size = scr.getmaxyx()
    for ri, st in enumerate(texture):
        for ci, cr in enumerate(st):
            r = pos[0] + ri
            c = pos[1] + ci
            if r >= 0 and c >= 0 and r < scr_size[0] and c < scr_size[1]:
                scr.addch(r, c, cr[0], color_pair_rgb(cr[1], cr[2], cr[3]))


def render_texture_a(scr, pos, texture):
    scr_size = scr.getmaxyx()
    for ri, st in enumerate(texture):
        for ci, cr in enumerate(st):
            r = pos[0] + ri
            c = pos[1] + ci
            if cr[1] > 0 and r >= 0 and c >= 0 and r < scr_size[0] and c < scr_size[1]:
                scr.addch(r, c, cr[0])


def render_texture_just_char(scr, pos, texture):
    scr_size = scr.getmaxyx()
    for ri, st in enumerate(texture):
        for ci, cr in enumerate(st):
            r = pos[0] + ri
            c = pos[1] + ci
            if r >= 0 and c >= 0 and r < scr_size[0] and c < scr_size[1]:
                scr.addch(r, c, cr[0])


def render_texture(scr, pos, texture):
    if len(texture[0][0]) == 5:
        render_texture_rgba(scr, pos, texture)
    elif len(texture[0][0]) == 4:
        render_texture_rgb(scr, pos, texture)
    elif len(texture[0][0]) == 2:
        render_texture_a(scr, pos, texture)
    elif len(texture[0][0]) == 1:
        render_texture_just_char(scr, pos, texture)



#ЗАПУСК:

def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
