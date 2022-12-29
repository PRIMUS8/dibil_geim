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
            self.current_sub_app = self.current_sub_app.run()


class SubApp:
    def __init__(self, scr):
        self.scr = scr

        self.current_event = [0, 0, None, None]

    def run(self):
        while True:
            return self

    def get_state(self):
        self.update_event()
        return self.current_event #TODO: блин надо придумать чтоб нормально

    def update_event(self):
        try:
            self.current_event[3] = self.scr.getkey()
        except curses.error:
            self.current_event[3] = None
        if self.current_event[3] == 'KEY_MOUSE':
            _, self.current_event[0], self.current_event[1], _, self.current_event[2] = self.scr.getmouse()
        else:
            self.current_event[2] = None


#ИГРА:

#Сущности:

pass


#Игра:

pass


#ИГРОВОЕ МЕНЮ:

#Виджеты:

class Widget:
    def __init__(self, scr, rpos, dpos, rsize, dsize):
        self.scr = scr
        self.rpos = rpos
        self.dpos = dpos
        self.rsize = rsize
        self.dsize = dsize

    def handle(self, event):
        self.draw()

    def draw(self):
        pass

    def get_pos(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rpos[0]) + self.dpos[0],
                int(scr_size[1] * self.rpos[1]) + self.dpos[1])

    def get_size(self):
        scr_size = self.scr.getmaxyx()
        return (int(scr_size[0] * self.rsize[0]) + self.dsize[0],
                int(scr_size[1] * self.rsize[1]) + self.dsize[1])


class Container(Widget):
    def __init__(self, scr, rpos, dpos, rsize, dsize):
        super().__init__(scr, rpos, dpos, rsize, dsize)


class Button(Widget):
    def __init__(self, scr, rpos, dpos, rsize, dsize, text):
        super().__init__(scr, rpos, dpos, rsize, dsize)
        self.text = text
        self.state = 'nothing'

    def handle(self, event):
        pos = self.get_pos()
        size = self.get_size()
        if event[0] >= pos[0] and event[1] >= pos[1] and event[0] < pos[0] + size[0] and event[1] < pos[1] + size[1]:
            if event[3] == curses.BUTTON1_PRESSED:
                self.state = 'clicked'
            else:
                self.state = 'selected'
        else:
            self.state = 'nothing'
        self.draw()

    def draw(self):
        if self.state == 'nothing':
            pass
        elif self.state == 'selected':
            pass
        elif self.state == 'clicked':
            pass


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
