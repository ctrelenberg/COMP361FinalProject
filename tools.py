__font = None

def get_font():
    import pygame
    global __font
    if __font is None:
        __font = pygame.font.SysFont('arial', 20)
    return __font


class PygameContext:
    def __init__(self, screen, surface, pg):
        self.screen = screen
        self.pg = pg

def get_user_input(loc, app, restraints=dict(), default='', prompt=''):
    p = app.pg
    s = app.screen
    f = app.text

    ret_str = str(default)
    key = None
    esc_keys = [p.key.name(k) for k in [p.K_RETURN, p.K_ESCAPE]]
    while key not in esc_keys:
        app.clock.tick(60)
        # s.blit(, (20,20))
        text = f.render(ret_str, 1, (0,0,0))
        s.blit(text, loc)
        t2 = f.render(prompt, 1, (0,0,0))
        s.blit(t2, (loc[0], loc[1] - 30))
        p.display.update()

        e = p.event.poll()
        keys_down = p.key.get_pressed()
        if e.type != p.KEYDOWN:
            continue

        key = p.key.name(e.key)
        # For now, just use trailing
        if key.startswith('keypad '):
            key = ' '.join(key.split(' ')[1:])

        if len(key) != 1:
            if key == "backspace":
                ret_str = ret_str[:len(ret_str) - 1]
            continue

        if keys_down[p.K_LSHIFT] or keys_down[p.K_RSHIFT]:
            ret_str += key.upper()
        else:
            ret_str += key

    if 'num' in restraints:
        try:
            r = int(ret_str)
            return r
        except:
            return default
    return ret_str
