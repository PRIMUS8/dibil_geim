#!/usr/bin/python


import curses, sys, os, ascii_renderer


#ПРИЛОЖЕНИЕ:

class App:
    def __init__(self):
        sys.stderr = open('./.errbuff', 'a')
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        sys.stderr.write(str(curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)) + '\n')
        curses.start_color()
        curses.curs_set(False)
        self.scr.nodelay(True)
        curses.halfdelay(1)
        ascii_renderer.init_pairs()

        self.current_sub_app = Menu(self.scr)
        self.event = None, 0, 0, None

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
            event = self.get_event()
            self.scr.clear()
            self.current_sub_app = self.current_sub_app.handle(event)
            self.scr.refresh()

    def get_event(self):
        try:
            kbevent = self.scr.getkey()
        except curses.error:
            kbevent = None
        if kbevent == 'KEY_MOUSE':
            _, x, y, _, bstate = curses.getmouse()
        else:
            x, y = self.event[1:3]
            bstate = None
        self.event = kbevent, x, y, bstate
        return self.event


class SubApp:
    def __init__(self, scr):
        self.scr = scr

    def handle(self, event):
        return self


#ИГРА:

#Сущности:

pass


#Игра:

pass


#ИГРОВОЕ МЕНЮ:

#Виджеты:

class Widget:
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, text, texture):
        self.scr = scr
        self.rltv_pos = rltv_pos
        self.dpos_pix = dpos_pix
        self.size_pix = size_pix
        self.text = text
        self.texture = texture

    def handle(self, event):
        self.draw()

    def draw(self):
        ascii_renderer.render_texture(self.scr, self.get_pos(), self.texture[0])

    def get_pos(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rltv_pos[0]) + self.dpos_pix[0],
                int(scr_size[1] * self.rltv_pos[1]) + self.dpos_pix[1])


class Button(Widget):
    def __init__(self, scr, rltv_pos, dpos_pix, size_pix, text):
        texture = ascii_renderer.load_texture('./ascii_textures/button')
        super().__init__(scr, rltv_pos, dpos_pix, size_pix, text, texture)
        self.state = 'nothing'

    def handle(self, event):
        self.draw()

    def draw(self):
        ascii_renderer.render_rectf_rgb(self.scr, self.get_pos(), self.size_pix, '#', (2, 2, 5))
        ascii_renderer.render_rectf_rgb(self.scr, (self.get_pos()[0] + 1, self.get_pos()[1] + 1), (self.size_pix[0] - 2, self.size_pix[1] - 2), '#', (0, 0, 0))


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
        widgets = [Button(scr, (0.2, 0.5), (-2, -10), (5, 20), ['BUTTON'])]
        super().__init__(scr, widgets)


class Menu(SubApp):
    def __init__(self, scr):
        super().__init__(scr)
        self.current_page = MainPage(self.scr)

    def handle(self, event):
        self.current_page = self.current_page.handle(event)
        return self


#ЗАПУСК:

def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
