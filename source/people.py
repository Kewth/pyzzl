'角色'

import curses
import time
import random
from pyzzl import data, screen

def make_xy_list(xmin, xmax, ymin, ymax):
    xy_list = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            xy_list.append((x, y))
    random.shuffle(xy_list)
    return xy_list

def walk_find(self, dis):
    def check(xmin, xmax, ymin, ymax, nx, ny):
        if not self.inmap.trygoto(self, nx, ny, True):
            return False
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                peo = self.inmap.get_people(x, y)
                if peo is not None and peo.camp != self.camp:
                    self.inmap.trygoto(self, nx, ny)
                    return True
        return False
    px, py = self.px, self.py
    if check(px - dis, px - 1, py - dis, py - 1, px - 1, py - 1): return
    if check(px - dis, px - 1, py, py, px - 1, py): return
    if check(px - dis, px - 1, py + 1, py + dis, px - 1, py + 1): return
    if check(px, px, py - dis, py - 1, px, py - 1): return
    if check(px, px, py + 1, py + dis, px, py + 1): return
    if check(px + 1, px + dis, py - dis, py - 1, px + 1, py - 1): return
    if check(px + 1, px + dis, py, py, px + 1, py): return
    if check(px + 1, px + dis, py + 1, py + dis, px + 1, py + 1): return

def freetime():
    return time.time() - freetime.skip
def freetime_lock():
    freetime.skip -= time.time()
def freetime_unlock():
    freetime.skip += time.time()
freetime.skip = 0

class base_people: # {{{
    def __init__(self, inmap, px, py, name, health, attack, speed, money, camp):
        self.inmap = inmap
        self.px = px
        self.py = py
        self.name = name
        self.health = health
        self.health_max = health
        self.attack = attack
        self.speed = speed
        self.money = money
        self.camp = camp
        self.clock = freetime()
        if inmap is not None:
            self.inmap.add_people(self)
        self.will_attack = False
        self.atk_xy_list = []
    def update_atk_xy_list(self):
        # 默认在 3x3 范围内搜索不同阵营的生物
        lis = make_xy_list(-1, 1, -1, 1)
        lis.remove((0, 0))
        self.atk_xy_list = []
        for xy in lis:
            dx, dy = xy
            peo = self.inmap.get_people(self.px + dx, self.py + dy)
            if peo is not None and peo.camp != self.camp:
                self.atk_xy_list = lis
                return
    def todo_attack(self):
        res = False
        if self.will_attack:
            res = True
            self.will_attack = False
            for xy in self.atk_xy_list:
                dx, dy = xy
                peo = self.inmap.get_people(self.px + dx, self.py + dy)
                peo_defence = False
                if peo is not None and peo.camp != self.camp:
                    peo_defence = not peo.gethurt(self.attack, self)
                if not peo_defence:
                    self.inmap.set_atk_map(self.px + dx, self.py + dy)
        else:
            self.update_atk_xy_list()
            if len(self.atk_xy_list) != 0:
                res = True
                self.will_attack = True
                self.clock += 0.8 - self.speed
        return res
    def todo_walk(self):
        for xy in make_xy_list(self.px - 1, self.px + 1, self.py - 1, self.py + 1):
            if self.inmap.trygoto(self, xy[0], xy[1]):
                return
    def todo(self):
        if freetime() > self.clock + self.speed:
            self.clock += self.speed
            if not self.todo_attack():
                self.will_attack = False
                self.todo_walk()
    def get_face(self):
        return screen.char('?')
    def gethurt(self, x, peo):
        self.health -= min(self.health, x)
        if self.health == 0:
            if peo is not None:
                peo.money += self.money
            self.money = 0
        return True
    def talk(self):
        screen.infobox('{}({})'.format(self.name, self.camp), ['!(#!(*%$*!@&$)(%*@', '(His language is unable to understand.)'])
    def getcure(self, x):
        self.health = min(self.health + x, self.health_max)
    def die(self):
        pass
# }}}

# pigs {{{
class pig (base_people):
    def __init__(self, inmap, px, py):
        base_people.__init__(self, inmap, px, py, 'Pig', 5, 2, 1.5, 2, 'Natural')
    def get_face(self):
        if self.will_attack:
            return screen.char('p', curses.COLOR_RED, curses.COLOR_BLACK)
        else:
            return screen.char('p')

class pig_fighter (base_people):
    def __init__(self, inmap, px, py):
        base_people.__init__(self, inmap, px, py, 'Pig soldier', 30, 4, 1.0, 10, 'Natural')
    def get_face(self):
        if self.will_attack:
            return screen.char('p')
        else:
            return screen.char('p', curses.COLOR_RED, curses.COLOR_BLACK)

class pig_king (base_people):
    def __init__(self, inmap, px, py):
        base_people.__init__(self, inmap, px, py, 'King of Pigs', 15, 0, 5.0, 5, 'Natural')
    def update_atk_xy_list(self):
        pass
    def todo_attack(self):
        res = False
        for xy in make_xy_list(self.px - 1, self.px + 1, self.py - 1, self.py + 1):
            x, y = xy
            if self.inmap.get_people(x, y) is None and self.inmap.floor_map[x][y].can_pass(self):
                res = True
                newpig = pig(self.inmap, x, y)
        return res
    def todo_walk(self):
        pass
    def gethurt(self, x, peo):
        self.health -= min(self.health, x)
        if self.health == 0:
            if peo is not None:
                peo.money += self.money
            self.money = 0
            if peo.__class__ == player:
                data.add_event('kill pig king')
        return True
    def get_face(self):
        return screen.char('P')

class pig_master (base_people):
    def __init__(self, inmap, px, py):
        base_people.__init__(self, inmap, px, py, 'Pig Master', 50, 4, 0.7, 30, 'Natural')
    def gethurt(self, x, peo):
        self.health -= min(self.health, x)
        if self.health == 0:
            if peo is not None:
                peo.money += self.money
            self.money = 0
            if peo.__class__ == player:
                data.add_event('kill pig master')
        return True
    def update_atk_xy_list(self):
        lis = make_xy_list(-2, 2, -2, 2)
        lis.remove((0, 0))
        lis.remove((-2, -2))
        lis.remove((-2, +2))
        lis.remove((+2, -2))
        lis.remove((+2, +2))
        self.atk_xy_list = []
        for xy in lis:
            dx, dy = xy
            peo = self.inmap.get_people(self.px + dx, self.py + dy)
            if peo is not None and peo.camp != self.camp:
                self.atk_xy_list = lis
                return
    def todo_walk(self):
        walk_find(self, 4)
    def get_face(self):
        if self.will_attack:
            return screen.char('P')
        else:
            return screen.char('P', curses.COLOR_RED, curses.COLOR_BLACK)

# }}}

class base_wave (base_people):
    def __init__(self, inmap, px, py, attack, master, dx, dy):
        base_people.__init__(self, inmap, px, py, 'Wave', 1, attack, 0.05, 0, master.camp)
        self.master = master
        self.dx = dx
        self.dy = dy
    def todo_attack(self):
        peo = self.inmap.get_people(self.px + self.dx, self.py + self.dy)
        if peo is None:
            return False
        self.health = 0
        if peo.camp == self.camp:
            return True
        peo_defence = not peo.gethurt(self.attack, self.master)
        if not peo_defence:
            self.inmap.set_atk_map(self.px + self.dx, self.py + self.dy)
        return True
    def todo_walk(self):
        if self.inmap.trygoto(self, self.px + self.dx, self.py + self.dy):
            return
        self.health = 0
    def get_face(self):
        if self.camp == 'Neutral':
            return screen.char('*', curses.COLOR_BLUE)
        else:
            return screen.char('*', curses.COLOR_RED)
    def gethurt(self, x, peo):
        if peo is None:
            return False
        self.health -= min(self.health, x)
        return True

class npc (base_people):
    def __init__(self, inmap, px, py, name):
        base_people.__init__(self, inmap, px, py, name, 10000, 0, 10.0, 0, 'Neutral')
    def todo(self):
        self.health = self.health_max
    def talk(self):
        screen.infobox('{}({})'.format(self.name, self.camp),
                # ['我不想和你废话。。。'])
                ['I am too tired to talk with you...'])
    def get_face(self):
        return screen.char('@')

class npc_white (npc): # {{{
    def __init__(self, inmap, px, py):
        npc.__init__(self, inmap, px, py, 'White')
    def talk(self):
        screen.infobox('{}({})'.format(self.name, self.camp),
                ['My name is white.', 'Maybe I can teach you what to do.',
                    'Remember check the exclamation marks first.',
                    'You can quit by press Ctrl-C any time and the archive will be saved automatically.',
                    'By the way, do you want to read archive or write archive? (r/w)'])
        screen.refresh()
        freetime_lock()
        cs = screen.choose('rw', True)
        freetime_unlock()
        if cs == ord('r'):
            name = screen.getstr(20, 5, 'type the archive name: ')
            if not data.init(name):
                screen.infobox('{}({})'.format(self.name, self.camp),
                        ['I am coufused.', 'The archive seems to be wrong.'])
        if cs == ord('w'):
            name = screen.getstr(20, 5, 'type the archive name: ')
            if not data.save(name):
                screen.infobox('{}({})'.format(self.name, self.camp),
                        ['I am coufused.'])
# }}}

class npc_pigger (npc): # {{{
    def __init__(self, inmap, px, py):
        npc.__init__(self, inmap, px, py, 'Pigger')
    def talk(self):
        screen.infobox('{}({})'.format(self.name, self.camp),
                # ['难以置信！我已经很长时间没有在这里见到其他人了。',
                #     '猪大师长廊过于疯狂，我认为没有什么人能够安全通过。',
                #     '对了，你可以在前方的存档点保存当前进度，这很有用。'])
                ['Unbelievable, I haven\'t seen any other humans here for a long time.',
                    'The Pig Master Avenue is crazy, I thought no one could pass it.',
                    'By the way, you can save your archive by crossing the archive point. It may be helpful.'])
# }}}

class npc_peter (npc): # {{{
    def __init__(self, inmap, px, py):
        npc.__init__(self, inmap, px, py, 'Peter')
    def talk(self):
        buy1 = data.get_event('shop 1')
        buy2 = data.get_event('shop 2')
        buy3 = data.get_event('shop 3')
        buy4 = data.get_event('shop 4')
        buy5 = data.get_event('shop 5')
        screen.infobox('{}({})'.format(self.name, self.camp),
                ['Hey, buddy.', 'I think you must want to buy something.', 'Donot worry, the shop is safe.',
                    '(1) New teleport point. ({})'.format('bought' if buy1 else 50),
                    '(2) Strength. ({})'.format('bought' if buy2 else 200),
                    '(3) Open the door. ({})'.format('bought' if buy3 else 100),
                    '(4) Maximum Health. ({})'.format('bought' if buy4 else 150),
                    '(5) {} ({})'.format(
                        'New teleport point.' if data.get_event('kill pig master') else '???',
                        'bought' if buy5 else 50),
                    ])
        screen.refresh()
        freetime_lock()
        cs = screen.choose('12345', True)
        freetime_unlock()
        if cs == ord('1'):
            if not buy1 and data.tryusemoney(50):
                data.add_event('shop 1')
                screen.infobox('{}({})'.format(self.name, self.camp), ['Now you can go back to Main City to check the new teleport.'])
            else:
                screen.infobox('{}({})'.format(self.name, self.camp), ['Humm... You must be kidding me.'])
        if cs == ord('2'):
            if not buy2 and data.tryusemoney(200):
                data.add_event('shop 2')
                data.register.peo.attack += 1
                screen.infobox('{}({})'.format(self.name, self.camp), ['Great.'])
            else:
                screen.infobox('{}({})'.format(self.name, self.camp), ['Humm... You must be kidding me.'])
        if cs == ord('3'):
            if not buy3 and data.tryusemoney(100):
                data.add_event('shop 3')
            else:
                screen.infobox('{}({})'.format(self.name, self.camp), ['Humm... You must be kidding me.'])
        if cs == ord('4'):
            if not buy4 and data.tryusemoney(150):
                data.add_event('shop 4')
                data.register.peo.health_max += 5
            else:
                screen.infobox('{}({})'.format(self.name, self.camp), ['Humm... You must be kidding me.'])
        if cs == ord('5'):
            if data.get_event('kill pig master') and not buy5 and data.tryusemoney(50):
                data.add_event('shop 5')
            else:
                screen.infobox('{}({})'.format(self.name, self.camp), [
                    'Humm... You must be kidding me.',
                    'Maybe you should kill the Pig Master.',
                    ])
# }}}

class player (base_people): # {{{
    def __init__(self):
        base_people.__init__(self, None, 0, 0, 'Adventurer', 20, 3, 0.0, 0, 'Neutral')
        self.magic = self.magic_max = 10
        self.magic_clock = time.time()
        self.mode = 'walk'
        self.keep_clock = 0
        self.events = set()
        self.direction = 'd'

    def todo (self):
        # 处理视野
        tmp_map = [[True for i in range(self.inmap.COL)] for i in range(self.inmap.LINE)]
        for x in range(self.inmap.LINE):
            for y in range(self.inmap.COL):
                # if not self.inmap.floor_map[x][y].can_see(self) or self.inmap.get_people(x, y) is not None:
                if not self.inmap.floor_map[x][y].can_see(self):
                    if x < self.px: x_list = range(x)
                    if x == self.px: x_list = [x - 1, x, x + 1]
                    if x > self.px: x_list = range(x + 1, self.inmap.LINE)
                    if y < self.py: y_list = range(y)
                    if y == self.py: y_list = [y - 1, y, y + 1]
                    if y > self.py: y_list = range(y + 1, self.inmap.COL)
                    for x2 in x_list:
                        for y2 in y_list:
                            if x2 in range(self.inmap.LINE) and y2 in range(self.inmap.COL):
                                tmp_map[x2][y2] = False
        tmp_map[self.px][self.py] = True

        px, py = 20, 20 # 打印中心
        for dx in range(screen.LINE):
            for dy in range(screen.COL):
                x = self.px + dx - px
                y = self.py + dy - py
                face = screen.char(' ')
                if x in range(self.inmap.LINE) and y in range(self.inmap.COL) and tmp_map[x][y]:
                    if time.time() < self.inmap.atk_map[x][y]:
                        face = screen.char('X', curses.COLOR_WHITE, curses.COLOR_RED)
                    else:
                        peo = self.inmap.get_people(x, y)
                        if peo == None:
                            face = self.inmap.floor_map[x][y].get_face()
                        else:
                            face = peo.get_face()
                screen.write_ch(dx, dy, face)

        while time.time() > self.magic_clock + 1:
            self.magic = min(self.magic + 1, self.magic_max)
            self.magic_clock += 1

        screen.write(1, 0, ' ' * 14)
        screen.write(2, 0, ' ' * 14)
        screen.write(3, 0, ' ' * 14)
        screen.write(0, 0, self.inmap.name + '|')
        screen.write(0, len(self.inmap.name), '|')
        screen.write(1, 0, '-' * len(self.inmap.name) + '+')
        screen.write(2, 0, 'HP: {}/{}'.format(self.health, self.health_max))
        screen.write(3, 0, 'MP: {}/{}'.format(self.magic, self.magic_max))
        screen.write(4, 0, 'ATK: {}'.format(self.attack))
        screen.write(5, 0, 'Mon: {}'.format(self.money))
        screen.write(6, 0, 'Mode: {}'.format(self.mode))
        screen.write(7, 0, 'Pos: {}, {}'.format(self.px, self.py))
        screen.write(1, 13, '+')
        screen.write(2, 13, '|')
        screen.write(3, 13, '|')
        screen.write(4, 13, '|')
        screen.write(5, 13, '|')
        screen.write(6, 13, '|')
        screen.write(7, 13, '|')
        screen.write(8, 0, '-' * 13 + '+')
        screen.refresh()

        def doattack(flag):
            def tryattack(x, y):
                peo = self.inmap.get_people(x, y)
                screen.write_ch(px + x - self.px, py + y - self.py, screen.char('X', curses.COLOR_WHITE, curses.COLOR_BLUE))
                if peo is not None:
                    peo.gethurt(self.attack, self)
            if flag == 'w':
                tryattack(self.px - 1, self.py)
                tryattack(self.px - 2, self.py)
            if flag == 's':
                tryattack(self.px + 1, self.py)
                tryattack(self.px + 2, self.py)
            if flag == 'd':
                tryattack(self.px, self.py + 1)
                tryattack(self.px, self.py + 2)
            if flag == 'a':
                tryattack(self.px, self.py - 1)
                tryattack(self.px, self.py - 2)
            self.mode = 'tired'
            self.keep_clock = time.time() + 0.3
            screen.refresh()
            time.sleep(0.1)

        def dospell(c):
            if self.magic < 3:
                self.mode = 'walk'
                return
            if c == ord('w'):
                dx, dy = -1, 0
            elif c == ord('s'):
                dx, dy = +1, 0
            elif c == ord('d'):
                dx, dy = 0, +1
            elif c == ord('a'):
                dx, dy = 0, -1
            else:
                self.mode = 'walk'
                return
            self.magic -= 3
            spell_atk = self.attack
            peo = self.inmap.get_people(self.px + dx, self.py + dy)
            self.mode = 'tired'
            self.keep_clock = time.time() + 0.2
            if peo is not None:
                screen.write_ch(px + dx, py + dy,
                        screen.char('X', curses.COLOR_WHITE, curses.COLOR_BLUE))
                peo.gethurt(spell_atk, self)
                screen.refresh()
                time.sleep(0.1)
            else:
                newwave = base_wave(self.inmap, self.px + dx, self.py + dy,
                        spell_atk, self, dx, dy)
                screen.refresh()

        def trytalk(x, y):
            if x in range(self.inmap.LINE) and y in range(self.inmap.COL):
                peo = self.inmap.get_people(x, y)
                if peo is not None:
                    peo.talk()
                else:
                    self.inmap.floor_map[x][y].talk()
            self.mode = 'walk'

        if time.time() > self.keep_clock:
            self.mode = 'walk'

        # c = screen.ifgetch(0.1)
        c = screen.ifgetch(0)
        if self.mode == 'tired':
            c = curses.ERR
        if c != curses.ERR and self.mode == 'spell':
            dospell(c)
            c = curses.ERR

        if c == ord('w'):
            if self.mode == 'attack':
                doattack('w')
            elif self.mode == 'talk':
                trytalk(self.px - 1, self.py)
            else:
                self.mode = 'walk'
                self.inmap.trygoto(self, self.px - 1, self.py)
            self.direction = 'w'
        if c == ord('s'):
            if self.mode == 'attack':
                doattack('s')
            elif self.mode == 'talk':
                trytalk(self.px + 1, self.py)
            else:
                self.mode = 'walk'
                self.inmap.trygoto(self, self.px + 1, self.py)
            self.direction = 's'
        if c == ord('d'):
            if self.mode == 'attack':
                doattack('d')
            elif self.mode == 'talk':
                trytalk(self.px, self.py + 1)
            else:
                self.mode = 'walk'
                self.inmap.trygoto(self, self.px, self.py + 1)
            self.direction = 'd'
        if c == ord('a'):
            if self.mode == 'attack':
                doattack('a')
            elif self.mode == 'talk':
                trytalk(self.px, self.py - 1)
            else:
                self.mode = 'walk'
                self.inmap.trygoto(self, self.px, self.py - 1)
            self.direction = 'a'
        if c == ord('j'):
            self.mode = 'attack'
            self.keep_clock = time.time() + 1
        if c == ord('h'):
            self.mode = 'spell'
            self.keep_clock = time.time() + 1
        if c == ord('t'):
            self.mode = 'talk'
            self.keep_clock = time.time() + 1
        if c == ord('k'):
            if self.mode == 'defence':
                self.mode = 'walk'
            else:
                self.mode = 'defence'
                self.keep_clock = time.time() + 0.4

    def gethurt(self, x, peo):
        if self.mode == 'defence':
            self.mode = 'tired'
            self.keep_clock = time.time() + 0.3
            return False
        self.health -= min(self.health, x)
        if self.health == 0:
            if peo is not None:
                peo.money += self.money
            self.money = 0
        return True

    def get_face(self):
        if self.mode == 'tired':
            return screen.char('@', curses.COLOR_YELLOW, curses.COLOR_BLUE)
        if self.mode == 'defence':
            return screen.char('@', curses.COLOR_WHITE, curses.COLOR_YELLOW)
        if self.mode == 'attack':
            return screen.char('@', curses.COLOR_RED, curses.COLOR_BLUE)
        return screen.char('@', curses.COLOR_WHITE, curses.COLOR_BLUE)
# }}}
