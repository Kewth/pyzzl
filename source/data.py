'数据'

import os
import copy
import json
from pyzzl import Map, screen

def register(peo):
    register.peo = peo
    register.px = 0
    register.py = 0
    register.inmap = None

def init(name):
    name = 'data/{}'.format(name)
    if not os.path.exists(name):
        return False
    peo = register.peo
    get = open(name, 'r')
    dic = json.load(get)
    if dic.get('inmap'):
        register.px = dic['px']
        register.py = dic['py']
        register.inmap = dic['inmap']
    for key in dic:
        val = dic[key]
        if key == 'events':
            val = set(val)
        peo.__dict__[key] = val
    peo.mode = 'walk'
    peo.keep_clock = 0
    return True

def save(name):
    name = 'data/{}'.format(name)
    peo = register.peo
    tar = open(name, 'w')
    dic = copy.copy(peo.__dict__)
    if register.inmap is not None:
        dic['px'] = register.px
        dic['py'] = register.py
        dic['inmap'] = register.inmap
    else:
        dic.pop('px')
        dic.pop('py')
        dic.pop('inmap')
    dic['events'] = list(dic['events'])
    json.dump(dic, tar)
    return True

def save_pos():
    peo = register.peo
    register.px = peo.px
    register.py = peo.py
    register.inmap = peo.inmap.name

def add_event(event):
    peo = register.peo
    if event not in peo.events:
        peo.events.add(event)
        screen.infobox('# New event #', [event])

def get_event(event):
    peo = register.peo
    return event in peo.events

def tryusemoney(mon):
    peo = register.peo
    if peo.money < mon:
        return False
    peo.money -= mon
    return True
