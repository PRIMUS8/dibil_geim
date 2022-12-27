import curses


def color_pair_fb(fb):
    return curses.color_pair((fb[0] + 1)*9 + fb[1] + 1)


def init_pairs_fb():
    for c1 in range(9):
        for c2 in range(9):
            curses.init_pair(c1*9 + c2, c1 - 1, c2 - 1)


def load_texture(path):
    try:
        texture = open(path, 'r').read()
    except FileNotFoundError:
        texture = open('./ascii_textures/default', 'r').read()
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


def render_texture_fba(scr, pos, size, texture):
    if size == 'texture':
        size = (len(texture), len(texture[0]))
    for r in range(pos[0], pos[0] + size[0]):
        for c in range(pos[1], pos[1]):
            ch = texture[r % len(texture)][c % len(texture[0])]
            if ch[4] > 0:
                try: scr.addch(r, c, ch[0], color_pair_fb(ch[1:3]))
                except curses.error: pass


def render_texture_a(scr, pos, size, texture):
    if size == 'texture':
        size = (len(texture), len(texture[0]))
    for r in range(pos[0], pos[0] + size[0]):
        for c in range(pos[1], pos[1]):
            ch = texture[r % len(texture)][c % len(texture[0])]
            if ch[-1] > 0:
                try: scr.addch(r, c, ch[0])
                except curses.error: pass


def render_texture(scr, pos, size, texture):
    if len(texture[0][0]) == 4:
        render_texture_fba(scr, pos, size, texture)
    elif len(texture[0][0]) == 2:
        render_texture_a(scr, pos, size, texture)


def render_rect(scr, pos, size, char, attrs):
    for ri in range(size[0]):
        try: scr.addstr(pos[0] + ri, pos[1], char*size[1], attrs)
        except curses.error: pass


def render_hrect(scr, pos, size, char, attrs):
    for ri in range(size[0]):
        if ri == size[0] or ri == 0:
            try: scr.addstr(pos[0] + ri, pos[1], char*size[1], attrs)
            except curses.error: pass
        else:
            try: scr.addch(pos[0] + ri, pos[1], char, attrs)
            except curses.error: pass
            try: scr.addch(pos[0] + ri, pos[1] + size[1], char, attrs)
            except curses.error: pass
