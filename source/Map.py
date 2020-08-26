'地图'

from pyzzl import floor, people, data

class base_map:
    def __init__(self, LINE, COL, name):
        self.LINE = LINE
        self.COL = COL
        self.name = name
        self.floor_map = [[None for i in range(COL)] for i in range(LINE)]
        self.people_list = set()
    def add_people (self, peo):
        self.people_list.add(peo)
    def remove_people(self, peo):
        self.people_list.remove(peo)
    def trygoto (self, peo, px, py):
        '检查 [peo] 是否能移动到 ([px], [py]) 并移动'
        test = px in range(self.LINE) and py in range(self.COL) and self.floor_map[px][py].can_pass(peo) and self.get_people(px, py) is None
        if test:
            peo.px = px
            peo.py = py
            self.floor_map[px][py].meet(peo)
        return test
    def get_people (self, px, py):
        for peo in self.people_list:
            if peo.px == px and peo.py == py:
                return peo
        return None

class main_city (base_map):
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
        if data.get_event('shop 1'):
            self.floor_map[0][0] = floor.trans(6, 0, spring_gallery)
        else:
            self.floor_map[0][0] = floor.trans(0, 0, spring_gallery)

class spring_gallery (base_map):
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
        for y in range(0, 5):
            self.floor_map[13][y] = floor.wall()
        # 传送点
        if data.get_event('shop 1'):
            self.floor_map[6][0] = floor.trans(0, 0, main_city)
        else:
            self.floor_map[0][0] = floor.trans(0, 0, main_city)
