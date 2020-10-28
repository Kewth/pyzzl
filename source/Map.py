'地图'

import time
import random
from pyzzl import floor, people, data

class base_map:
    def __init__(self, LINE, COL, name):
        self.LINE = LINE
        self.COL = COL
        self.name = name
        self.floor_map = [[None for i in range(COL)] for i in range(LINE)]
        self.atk_map = [[0 for i in range(COL)] for i in range(LINE)]
        self.people_list = set()
    def add_people (self, peo):
        self.people_list.add(peo)
    def remove_people(self, peo):
        self.people_list.remove(peo)
    def trygoto (self, peo, px, py, onlycheck = False):
        '检查 [peo] 是否能移动到 ([px], [py]) 并移动'
        test = px in range(self.LINE) and py in range(self.COL) and self.floor_map[px][py].can_pass(peo) and self.get_people(px, py) is None
        if test and not onlycheck:
            peo.px = px
            peo.py = py
            self.floor_map[px][py].meet(peo)
        return test
    def set_atk_map(self, px, py):
        if px in range(self.LINE) and py in range(self.COL):
            self.atk_map[px][py] = time.time() + 0.2
    def get_people(self, px, py):
        for peo in self.people_list:
            if peo.px == px and peo.py == py:
                return peo
        return None
    def todo(self):
        pass

class main_city (base_map): # {{{
    def __init__(self):
        base_map.__init__(self, 50, 80, 'Main City')
        for x in range(self.LINE):
            for y in range(self.COL):
                self.floor_map[x][y] = floor.grass()
        # 泉水
        self.floor_map[2][2] = floor.spa()
        self.floor_map[2][3] = floor.spa()
        self.floor_map[3][2] = floor.spa()
        self.floor_map[3][3] = floor.spa()
        self.floor_map[4][1] = floor.spa()
        self.floor_map[4][2] = floor.spa()
        self.floor_map[4][3] = floor.spa()
        self.floor_map[4][4] = floor.spa()
        self.floor_map[5][3] = floor.spa()
        self.floor_map[5][6] = floor.info(['Notice the pig.', 'They will attack you if you are close to them.',
            'But you can press "j" to hit back.', 'Go to the spring and you can get relax.'])
        people.pig(self, 6, 6)
        people.npc_white(self, 0, 5)
        # 猪祭坛
        people.pig_king(self, 20, 20)
        for x in range(0, 2):
            for y in range(4, 7):
                self.floor_map[x][y] = floor.camp_grass('Neutral')
        for x in range(17, 24):
            for y in range(17, 24):
                self.floor_map[x][y] = floor.trap()
        self.floor_map[16][16] = floor.wall()
        self.floor_map[16][17] = floor.wall()
        self.floor_map[16][23] = floor.wall()
        self.floor_map[16][24] = floor.wall()
        self.floor_map[17][16] = floor.wall()
        self.floor_map[17][24] = floor.wall()
        self.floor_map[23][16] = floor.wall()
        self.floor_map[23][24] = floor.wall()
        self.floor_map[24][16] = floor.wall()
        self.floor_map[24][17] = floor.wall()
        self.floor_map[24][23] = floor.wall()
        self.floor_map[24][24] = floor.wall()
        self.floor_map[15][15] = floor.info(['In front of you is the king\'s altar.', 'Notice the trap, once you touch it you will get hurted.'])
        # 传送点
        for x in range(1, self.LINE, 2):
            self.floor_map[x][0] = floor.empty()
        if data.get_event('shop 1'):
            self.floor_map[0][0] = floor.trans(6, 0, spring_gallery)
        else:
            self.floor_map[0][0] = floor.trans(0, 0, spring_gallery)
        if data.get_event('shop 5'):
            self.floor_map[2][0] = floor.trans(0, 2, pig_master_avenue)
# }}}

class spring_gallery (base_map): # {{{
    def __init__(self):
        base_map.__init__(self, 100, 5, 'Spring Gallery')
        for x in range(self.LINE):
            for y in range(self.COL):
                self.floor_map[x][y] = floor.spa()
        # 猪战士
        for y in range(0, 4):
            self.floor_map[1][y] = floor.wall()
        self.floor_map[1][4] = floor.event_door('kill pig king')
        for y in range(1, 5):
            self.floor_map[3][y] = floor.wall()
        self.floor_map[3][0] = floor.event_door('kill pig king')
        for y in range(0, 4):
            self.floor_map[5][y] = floor.wall()
        self.floor_map[5][4] = floor.event_door('kill pig king')
        people.pig_fighter(self, 2, 0)
        people.pig_fighter(self, 4, 0)
        people.pig_fighter(self, 4, 1)
        # 商店
        for y in range(1, 5):
            self.floor_map[9][y] = floor.wall()
        self.floor_map[9][0] = floor.event_door('shop 3')
        people.npc_peter(self, 7, 4)
        # 空地
        for x in range(10, 15):
            for y in range(0, 5):
                self.floor_map[x][y] = floor.grass()
        for y in range(1, 5):
            self.floor_map[10][y] = floor.wall()
        for y in range(0, 4):
            self.floor_map[15][y] = floor.wall()
            self.floor_map[16][y] = floor.wall()
        self.floor_map[15][4] = floor.event_door('kill pig master')
        self.floor_map[16][4] = floor.event_door('kill pig master')
        self.floor_map[17][0] = floor.trans(6, 0, None)
        for y in range(0, 5):
            self.floor_map[18][y] = floor.wall()
        self.floor_map[10][0] = floor.once_door()
        people.pig_master(self, 11, 4)
        # 传送点
        if data.get_event('shop 1'):
            self.floor_map[6][0] = floor.trans(0, 0, main_city)
        else:
            self.floor_map[0][0] = floor.trans(0, 0, main_city)
# }}}

class pig_master_avenue (base_map): # {{{
    def __init__(self):
        base_map.__init__(self, 50, 5, 'Pig Master Avenue')
        for x in range(self.LINE):
            self.floor_map[x][0] = floor.grass()
            self.floor_map[x][2] = floor.spa()
            self.floor_map[x][4] = floor.grass()
            if x % 3 == 2:
                self.floor_map[x][1] = floor.wall()
                self.floor_map[x][3] = floor.wall()
            else:
                self.floor_map[x][1] = floor.empty()
                self.floor_map[x][3] = floor.empty()
            people.pig_master(self, x, 0)
            people.pig_master(self, x, 4)
        # 传送点
        self.floor_map[0][2] = floor.trans(2, 0, main_city)
        self.floor_map[49][2] = floor.trans(0, 0, ancient_palace)
# }}}

class ancient_palace (base_map): # {{{
    def __init__(self):
        charmap = '''
1.@......     2...........          3............
...     ..          .             ...            
..A      ..         .            ..              
.         ..        .            .               
.          .        .            .               
.          .        .            .               
.         ..        .            .               
.     .....         .            .               
.......             .            .               
.                   .            .               
.                   .            .               
.                   .            .               
.                   .            .               
.  #######          .            .         ......
.  //////#          .            .        .. .  .
.  ~~~~~/#          .            .       ..     .
.??~~~~~/#          .            .              .
.??~~~~~/#          .            .              .
.  ~~~~~/#          .            ..             .
.  ////?/#          .             .            ..
4  ####5##   ...............      .............. 
'''[1:-1].split('\n')
        base_map.__init__(self, len(charmap), len(charmap[0]), 'Ancient Palace')
        for x in range(self.LINE):
            for y in range(self.COL):
                if charmap[x][y] == '.':
                    self.floor_map[x][y] = floor.grass()
                elif charmap[x][y] == ' ':
                    self.floor_map[x][y] = floor.empty()
                elif charmap[x][y] == '~':
                    self.floor_map[x][y] = floor.spa()
                elif charmap[x][y] == '#':
                    self.floor_map[x][y] = floor.wall()
                elif charmap[x][y] == '?':
                    self.floor_map[x][y] = floor.hide_grass()
                elif charmap[x][y] == '/':
                    self.floor_map[x][y] = floor.hide_wall()
                elif charmap[x][y] == 'A':
                    self.floor_map[x][y] = floor.archive_point()
                elif charmap[x][y] == '1':
                    self.floor_map[x][y] = floor.trans(49, 2, pig_master_avenue)
                elif charmap[x][y] == '2':
                    self.floor_map[x][y] = floor.trans(49, 2, pig_master_avenue)
                elif charmap[x][y] == '3':
                    self.floor_map[x][y] = floor.trans(49, 2, pig_master_avenue)
                elif charmap[x][y] == '4':
                    self.floor_map[x][y] = floor.trans(2, 0, main_city)
                elif charmap[x][y] == '5':
                    self.floor_map[x][y] = floor.trans(1, 4, palace_secret_room)
                elif charmap[x][y] == '@':
                    self.floor_map[x][y] = floor.grass()
                    people.npc_pigger(self, x, y)
# }}}

class palace_secret_room (base_map): # {{{
    def __init__(self):
        charmap = '''
###########################################
#p .1. p###2............  ............###.#
#  ...  ####............  ............###.#
#.......####............  ............###.#
#... ...####............PP............###.#
#.......####............  ............###.#
#  ...  ####............  ............###.#
#p ... p####............  ................#
###########################################
'''[1:-1].split('\n')
        base_map.__init__(self, len(charmap), len(charmap[0]), 'Secret Room of Ancient Palace')
        for x in range(self.LINE):
            for y in range(self.COL):
                if charmap[x][y] == '.':
                    self.floor_map[x][y] = floor.grass()
                elif charmap[x][y] == ' ':
                    self.floor_map[x][y] = floor.empty()
                elif charmap[x][y] == '#':
                    self.floor_map[x][y] = floor.wall()
                elif charmap[x][y] == 'p':
                    self.floor_map[x][y] = floor.grass()
                    people.pig(self, x, y)
                elif charmap[x][y] == 'P':
                    self.floor_map[x][y] = floor.grass()
                    people.pig_master(self, x, y)
                elif charmap[x][y] == '1':
                    self.floor_map[x][y] = floor.trans(20, 7, ancient_palace)
                elif charmap[x][y] == '2':
                    self.floor_map[x][y] = floor.trans(4, 4, None)
        self.change_clock = time.time() + 2
    def todo(self):
        def has_pig():
            for peo in self.people_list:
                if peo.__class__ == people.pig:
                    return True
        if not has_pig():
            self.floor_map[4][4] = floor.trans(1, 11, None)
        if time.time() > self.change_clock:
            self.change_clock += 2
            for x in range(1, 8):
                for y in range(12, 38):
                    if y != 24 and y != 25:
                        if random.randint(1, 100) <= 10:
                            # self.floor_map[x][y] = floor.trans(1, 11, None)
                            self.floor_map[x][y] = floor.low_wall()
                        else:
                            self.floor_map[x][y] = floor.grass()
# }}}
