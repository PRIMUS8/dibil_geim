#!/usr/bin/python


import curses, sys, os, ascii_renderer


#ПРИЛОЖЕНИЕ:

class App:
    def __init__(self):
        sys.stderr = open('./.errbuff', 'a')
        os.environ['TERM'] = 'xterm-1003'

        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)

        self.scr.nodelay(True)
        curses.halfdelay(1)

        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)
        ascii_renderer.init_pairs_fb()

        curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
        curses.mouseinterval(0)

        self.current_sub_app = Menu(self.scr)
        self.event = 0, 0, None, None

    def __del__(self):
        self.scr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        sys.stderr = sys.__stderr__
        sys.stderr.write(open('./.errbuff', 'r').read())
        os.remove('./.errbuff')

    def run(self):
        while True:
            self.update_event()
            self.scr.clear()
            self.current_sub_app = self.current_sub_app.handle(self.event)
            self.scr.refresh()

    def update_event(self):
        try:
            key = self.scr.getkey()
        except curses.error:
            key = None
        if key == 'KEY_MOUSE':
            _, x, y, _, bstate = curses.getmouse()
        else:
            y, x = self.event[0:2]
            bstate = None
        self.event = y, x, bstate, key


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
    def __init__(self, scr, rltv_pos, dpos_pix, rltv_size, dsize_pix, text, texture):
        self.scr = scr
        self.rltv_pos = rltv_pos
        self.dpos_pix = dpos_pix
        self.rltv_size = rltv_size
        self.dsize_pix = dsize_pix
        self.text = text
        self.texture = texture

    def handle(self, event):
        self.draw()

    def draw(self):
        ascii_renderer.render_texture(self.scr, self.get_pos(), self.get_size(), self.texture[0])

    def get_pos(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rltv_pos[0]) + self.dpos_pix[0],
                int(scr_size[1] * self.rltv_pos[1]) + self.dpos_pix[1])

    def get_size(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rltv_size[0]) + self.dsize_pix[0],
                int(scr_size[1] * self.rltv_size[1]) + self.dsize_pix[1])


class Button(Widget):
    def __init__(self, scr, rltv_pos, dpos_pix, rltv_size, dsize_pix, text):
        texture = ascii_renderer.load_texture('./ascii_textures/button')
        super().__init__(scr, rltv_pos, dpos_pix, rltv_size, dsize_pix, text, texture)
        self.state = 'nothing'

    def handle(self, event):
        pos = self.get_pos()
        size = self.get_size()
        if event[0] >= pos[0] and event[1] >= pos[1] and event[0] < pos[0] + size[0] and event[1] < pos[1] + size[1]:
            self.state = 'selected'
        else:
            self.state = 'nothing'
        self.draw()

    def draw(self):
        if self.state == 'nothing':
            ascii_renderer.render_rect(self.scr, self.get_pos(), self.get_size(), '#', ascii_renderer.color_pair_fb((0, 5)))
            ascii_renderer.render_rect(self.scr, (self.get_pos()[0] + 1, self.get_pos()[1] + 1),
                                        (self.get_size()[0] - 2, self.get_size()[1] - 2), '[', ascii_renderer.color_pair_fb((0, 2)))
        elif self.state == 'selected':
            ascii_renderer.render_rect(self.scr, self.get_pos(), self.get_size(), '#', ascii_renderer.color_pair_fb((0, 5)))
            ascii_renderer.render_rect(self.scr, (self.get_pos()[0] + 1, self.get_pos()[1] + 1),
                                        (self.get_size()[0] - 2, self.get_size()[1] - 2), ']', ascii_renderer.color_pair_fb((0, 3)))
        elif self.state == 'clicked':
            ascii_renderer.render_rect(self.scr, self.get_pos(), self.get_size(), '#', ascii_renderer.color_pair_fb((0, 5)))
            ascii_renderer.render_rect(self.scr, (self.get_pos()[0] + 1, self.get_pos()[1] + 1),
                                        (self.get_size()[0] - 2, self.get_size()[1] - 2), ':', ascii_renderer.color_pair_fb((0, 5)))
        self.scr.addstr(self.get_pos()[0] + int(self.get_size()[0]/2), self.get_pos()[1] + int(self.get_size()[1]/2) - int(len(self.text[0])/2), self.text[0], ascii_renderer.color_pair_fb((0, 5)))


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
        widgets = [Button(scr, (0.2, 0.25), (2, 2), (0.5, 0.5), (-2, -2), ['BUTTON'])]
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
