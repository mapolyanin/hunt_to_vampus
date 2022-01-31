import random

GRAF = {
    1:{2, 5, 6}, #a
    2:{1, 8, 3}, #b
    3:{2, 4, 10}, #c
    4:{3, 5, 12}, #d
    5:{4, 1, 14}, #e
    6:{1, 7, 15}, #f
    7:{6, 8, 16}, #g
    8:{7, 9, 2}, #h
    9:{8, 10, 17}, #i
    10:{9, 11, 3}, #j
    11:{10, 12, 18}, #k
    12:{11, 13, 4}, #l
    13:{12, 14, 19}, #m
    14:{13, 15, 5}, #n
    15:{14, 6, 20}, #o
    16:{20, 17, 7}, #p
    17:{16, 18, 9}, #q
    18:{17, 19, 11}, #r
    19:{18, 20, 13}, #s
    20:{19, 16, 15}, #t
}
LIFE = 1
ARROWS = 7
BATS = 2
DEEPS = 2
random.seed(1000)

class Map():
    def __init__(self):
        self.maze = dict()
        self.deeps = []
        self.bats = []
        self.vampus_died = False
        self.vampuses_room = None
        self.players_room = None
        self.arrows = ARROWS

    def start_game(self):
        _unused_rooms = set(GRAF.keys())
        #set vampus
        self.vampuses_room = random.choice(list(_unused_rooms))
        _unused_rooms.discard(self.vampuses_room)
        
        #set bats
        for i in range(0, BATS):
            room = random.choice(list(_unused_rooms))
            self.bats.append(room)
            _unused_rooms.discard(room)
            
        #set deeps
        for i in range(0, DEEPS):
            room = random.choice(list(_unused_rooms))
            self.deeps.append(room)
            _unused_rooms.discard(room)
        
        #set player in room, where not vampus, bats, deeps, and bad neighbors ))
        #найти хорошие комнаты (не соседствующие с ямами, вампусом и мышами)
        #найти комнаты, где уже ктото есть
        _used_rooms = set(GRAF.keys()).difference(_unused_rooms)
        
        for i in _used_rooms:
            for k in GRAF[i]:
                _unused_rooms.discard(k)

        self.players_room = random.choice(list(_unused_rooms))
        
        for i in GRAF.keys():
            self.maze[i] = Room(room_number=i, 
            next_room=GRAF[i])

        for i in self.deeps:
            self.maze[i].deep = True

        for i in self.bats:
            self.maze[i].bat = True

    def get_smell(self, room):
        for i in self.maze[room].next_room:
            if i == self.vampuses_room:
                return True
        return False
        

    def get_breeze(self, room):
        #получаем информацию, есть ли тут ветерок. Берем как положено, из Room
        for i in self.maze[room].next_room:
            if self.maze[i].deep == True:
                return True
        return False
        

    def get_noise(self, room):
        for i in self.maze[room].next_room:
            if self.maze[i].bat == True:
                return True
        return False
        
    def action(self):
        pass

    def game_over(self):
        pass



class Room():
    """Data-class for data about room"""
    def __init__(self, room_number:int, next_room:set) -> None:
        self.room_number = room_number
        self.next_room = next_room
        self.deep = False
        self.bat = False
    

class Unit():
    def __init__(self, map):
        self.position = None
        self.live = True
        self.map = map

    def move(self, target):
        pass
    
    def next_rooms(self):
        pass

    def fire(self):
        pass

    def random_move(self, target, limit):
        pass

    
class Player(Unit):
    def __init__(self, arrows:int, map: object, life:int = 1,):
        self.arrows = arrows
        #self.room = room
        self.life = life
    
    def fire(self, map, room):
        
        pass


    def get_next_rooms(self):
        pass

    def move(self):
        pass


    pass

class Vampus(Unit()):

    def fear_arrow(self):
        if random.choice([1,2,3,4]) == 1:
           self.random_move()
    

class Logic():
    pass