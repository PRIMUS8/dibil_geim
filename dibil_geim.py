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

        self.current_sub_app = Menu(self.scr)

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
        while True:
            self.scr.erase()
            self.current_sub_app = self.current_sub_app.handle(self.get_event())
            self.scr.refresh()

    def get_event(self):
        try:
            event = self.scr.getkey()
        except curses.error:
            event = None
        _, x, y, _, bstate = curses.getmouse()
        return event, x, y, bstate


class SubApp:
    def __init__(self, scr):
        self.scr = scr

    def handle(self, event):
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

    def handle(self, event):
        self.draw()

    def draw(self):
        render_texture(self.scr, self.get_pos(), self.texture[0])

    def get_pos(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rltv_pos[0]) + self.dpos_pix[0],
                int(scr_size[1] * self.rltv_pos[1]) + self.dpos_pix[1])


class Button(Widget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, texture):
        super().__init__(scr, rltv_pos, dpos_pix, size_pix, texture)
        self.state = 'nothing'

    def handle(self, event):
        self.draw()


#Страницы меню:

class Page:
    def __init__(self, scr, widgets):
        self.scr = scr
        self.widgets = widgets

    def handle(self, event):
        for widget in self.widgets:
            widget.handle(event)
        return self


class GameConfig(Page):
    def __init__(self, scr):
        widgets = []
        super().__init__(scr, widgets)


class Settings(Page):
    def __init__(self, scr):
        widgets = []
        super().__init__(scr, widgets)


class MainPage(Page):
    def __init__(self, scr):
        widgets = []
        super().__init__(scr, widgets)


class Menu(SubApp):
    def __init__(self, scr):
        super().__init__(scr)
        self.current_page = MainPage(self.scr)

    def handle(self, event):
        self.current_page = self.current_page.handle(event)
        return self


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
