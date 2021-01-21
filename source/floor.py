'地面'

import sys
import curses
from pyzzl import screen, people, data

class base_floor:
    def __init__(self):
        pass
    def meet (self, peo):
        pass
    def talk (self):
        pass
    def can_pass(self, peo):
        return True
    def can_see(self, peo):
        return True
    def get_face(self):
        return screen.char('?')

class grass (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def get_face(self):
        return screen.char('.', curses.COLOR_GREEN, curses.COLOR_BLACK)

class wall (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def can_pass(self, peo):
        return False
    def can_see(self, peo):
        return False
    def get_face(self):
        return screen.char('#', curses.COLOR_YELLOW, curses.COLOR_BLACK)

class low_wall (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def can_pass(self, peo):
        return False
    def get_face(self):
        return screen.char('=', curses.COLOR_YELLOW, curses.COLOR_BLACK)

class trap (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def meet (self, peo):
        peo.gethurt(1, None)
    def get_face(self):
        return screen.char('.', curses.COLOR_RED, curses.COLOR_BLACK)

class spa (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def meet (self, peo):
        peo.getcure(1)
    def get_face(self):
        return screen.char('~', curses.COLOR_BLUE, curses.COLOR_BLACK)

class info (base_floor):
    def __init__(self, text_list):
        base_floor.__init__(self)
        self.text_list = text_list
    def meet (self, peo):
        if peo.__class__ == people.player:
            screen.infobox('Notice', self.text_list)
    def get_face(self):
        return screen.char('!')

class empty (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def can_pass(self, peo):
        return False
    def get_face(self):
        return screen.char(' ')

class trans (base_floor):
    def __init__(self, newx, newy, newmap):
        base_floor.__init__(self)
        self.newx = newx
        self.newy = newy
        self.newmap = newmap
    def meet(self, peo):
        if peo.__class__ == people.player:
            peo.px = self.newx
            peo.py = self.newy
            if self.newmap:
                peo.inmap = self.newmap # only a class
    def get_face(self):
        return screen.char('O', curses.COLOR_BLUE, curses.COLOR_WHITE)

class camp_grass (base_floor):
    def __init__(self, camp):
        base_floor.__init__(self)
        self.camp = camp
    def can_pass(self, peo):
        return peo.camp == self.camp
    def get_face(self):
        if self.camp == 'Neutral':
            return screen.char('+', curses.COLOR_GREEN, curses.COLOR_BLACK)
        else:
            return screen.char('+', curses.COLOR_YELLOW, curses.COLOR_BLACK)

class event_door (base_floor):
    def __init__(self, event):
        base_floor.__init__(self)
        self.event = event
    def can_pass(self, peo):
        return peo.__class__ == people.player and data.get_event(self.event)
    def talk(self):
        screen.infobox('', ['You need event "{}" to pass it.'.format(self.event)])
    def get_face(self):
        if data.get_event(self.event):
            return screen.char('+', curses.COLOR_GREEN, curses.COLOR_BLACK)
        else:
            return screen.char('+', curses.COLOR_YELLOW, curses.COLOR_BLACK)

class once_door (base_floor):
    def __init__(self):
        base_floor.__init__(self)
        self.open = True
    def can_pass(self, peo):
        return self.open and peo.__class__ == people.player
    def meet(self, peo):
        if peo.__class__ == people.player:
            self.open = False
    def talk(self):
        if not self.open:
            screen.infobox('', ['It is closed now.'])
    def get_face(self):
        if self.open:
            return screen.char('.', curses.COLOR_GREEN, curses.COLOR_BLACK)
        else:
            return screen.char('+', curses.COLOR_YELLOW, curses.COLOR_BLACK)

class hide_grass (grass):
    def __init__(self):
        grass.__init__(self)
    def get_face(self):
        return screen.char(' ')

class hide_wall (wall):
    def __init__(self):
        wall.__init__(self)
    def get_face(self):
        return screen.char(' ')

class archive_point (base_floor):
    def __init__(self):
        base_floor.__init__(self)
    def meet (self, peo):
        if peo.__class__ == people.player:
            screen.infobox('Archive point', ['Your position is saved', 'And the archive is saved to "{}".'.format(data.init.name)])
            data.save_pos()
            data.save()
    def get_face(self):
        return screen.char('A', curses.COLOR_WHITE, curses.COLOR_YELLOW)
