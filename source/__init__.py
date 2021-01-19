'初始化'

import os
import time
import curses
from pyzzl import screen, data, Map, floor, people

def work(stdscr):
    try:
        LINE, COL = 40, 130
        if screen.init(stdscr, LINE, COL) == False:
            screen.write(0, 0, 'Screen too small. Only {}x{} but {}x{} is needed.'.format(curses.LINES, curses.COLS, LINE, COL))
            screen.refresh(False)
            time.sleep(1)
            return
        player = people.player()
        data.register(player)
        if os.path.exists('data/default'):
            data.init('default')
        if player.inmap == None:
            city = Map.main_city()
            player.px = 5
            player.py = 5
        else:
            dic = {
                    'Main City': Map.main_city,
                    'Spring Galery': Map.spring_gallery,
                    'Pig Master Avenue': Map.pig_master_avenue,
                    'Ancient Palace': Map.ancient_palace,
                    'Secret Room of Ancient Palace': Map.palace_secret_room,
                    'Secret Room of Ancient Palace 2': Map.palace_secret_room_2,
                    }
            city = dic[player.inmap]()
        player.inmap = city
        city.add_people(player)
        screen.clear()
        screen.write(20, 20, city.name)
        screen.refresh()
        time.sleep(1)
        while player in city.people_list:
            people_list = list(city.people_list)
            for peo in people_list:
                if peo.health == 0:
                    peo.die()
                    city.remove_people(peo)
                else:
                    peo.todo()
            if player.inmap != city:
                city = player.inmap()
                player.inmap = city
                city.add_people(player)
                screen.clear()
                screen.write(20, 20, city.name)
                screen.refresh(False)
                time.sleep(1)
            else:
                city.todo()
        screen.clear()
        screen.write(20, 20, 'You are dead.')
        screen.write(21, 20, 'Aricheve is not saved.')
        screen.refresh(False)
        time.sleep(1)
    except KeyboardInterrupt:
        data.save('default')
        screen.clear()
        screen.write(20, 20, 'See you next time.')
        screen.write(21, 20, 'Aricheve is saved.')
        screen.refresh(False)
        time.sleep(1)

def main():
    curses.wrapper(work)

