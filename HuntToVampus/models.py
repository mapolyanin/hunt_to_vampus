import random
from shutil import move

#map of game.
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
random.seed(1000) #comment this after debugging and refactoring

class Map():
    """
    This is main class of game. 
    """
    def __init__(self):
        self.maze = dict()
        self.deeps = []
        self.bats = []
        #self.vampus_died = False
        self.vampuses_room = None
        self.players_room = None
        self.arrows = ARROWS

    def start_game(self):
        """
        this metod MAST be called before game
        """
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

    def get_smell(self, room:int) -> bool:
        """
        Call this metod for smelled vampus
        """
        for i in self.maze[room].next_room:
            if i == self.vampuses_room:
                return True
        return False
        

    def get_breeze(self, room:int) -> bool:
        """
        Call this metod for feel breeze... from deep
        """
        for i in self.maze[room].next_room:
            if self.maze[i].deep == True:
                return True
        return False
        

    def get_noise(self, room):
        """
        Call this metod to hear the noize from bat
        """
        for i in self.maze[room].next_room:
            if self.maze[i].bat == True:
                return True
        return False
        
    def action(self, fire:bool, move:bool, target:int):
        """
        This metod return result of users action.


        """

        #this stait after action
        self.result = {'vampus_died':False,
                   'player_died':False, 
                   'win':False,
                   'lose':False, 
                   'bat_detect':False, 
                   'deep_detect':False,
                   'empty_room': False,
                   'bat_transfer':0,
                   'player_meet_vampus':False, 
                   'vampus_meet_player':False,
                   'deep': False,
                   'no_arrows': False, 
                   'vampus_fear':False
                   }

        #validated
        if (fire ^ move):
            pass
        else:
            return None

        if target in self.maze[self.players_room].next_room:
            pass
        else:
            return None

        #Начинаем действие и реакцию на него

        if move:
            #move_player in next room
            self.players_room = target
        
        if self.maze[self.players_room].bat:
            #action, if in new room live bat
            while True:
                new_room = random.choice(self.maze)
                if new_room.bat:
                    continue
                else:
                    self.players_room = new_room.room_number
                    break
            self.result['bat_transfer'] = new_room.room_number
        
        if self.players_room == self.vampuses_room:
            self.result['player_meet_vampus'] = True
            self.result['player_died'] = True
        

        if self.maze[self.players_room].deep:
            #player is died in deep
            self.result['deep'] = True
            self.result['player_died'] = True
            self.result['lose'] = True

        if fire:
            #if player fired
            self.arrows -=1
            if target == self.vampuses_room:
                #we died vampus!
                self.result ['vampus_died'] = True
                self.result['win'] = True
            elif self.maze[target].bat:
                #bat detect in target room
                self.result ['bat_detect']= True
            elif self.maze[target].deep:
                #deep detect in target room
                self.result ['deep_detect']=True
            else:
                #empty room
                self.result['empty_room']=True
            

            #vampus wake up after fire...may be 
            if random.choice(range(0,4)) in [0,1]:
                self.result['vampus_fear'] = True
                #перемещаем вампуса в соседнюю комнату. Если там мыши или пропасть, он там спать не будет, и пойдет дальше.
                while True:
                    new_room = random.choice(list(self.maze[self.vampuses_room].next_room))
                    self.vampuses_room = new_room
                    if (self.maze[self.vampuses_room].bat or self.maze[self.vampuses_room].deep):
                        continue
                    else:
                        break
                if self.vampuses_room == self.players_room:
                    #player is tourist breakfast for vampus
                    self.result['vampus_meet_player'] = True
                    self.result['player_died'] = True
                    self.result['lose'] = True
        
            
        if self.arrows == 0:
            #if arrows is out, game is over
            
            self.result['no_arrows'] = True
            self.result['lose'] = True
               
        return self.result

        """
        Принимает действие пользователя из основного модуля, проверяет на валидность, возвращает словарь с результатом действия.byb
        Принимаемые значения:
        {'move':bool, 'fire':bool, target:int}
        Возвращаемое значение:
        {vampus_died:bool, player_died:bool, win:bool, 
        lose:bool, bat_detect:bool, deep_detect:bool, bat_transfer:int,
        player_meet_vampus:bool, vampus_meet_player:bool} 
        или 
        None если переданы некорректные данные.

        Возможная реакция системы:
        Пользователь в комнате летучих мышей. Летучаея мышь переносит пользователя в случайную другую комнату. Проверка условий продолжается.
        Пользователь в комнате вампуса. Вампус убивает пользователя. Игра окончена.
        Пользователь в комнате с пропастью. Пользователь погибает. Игра окончена.
        Пользователь стреляет в комнату с вампусом. Вампус погибает. Игрок побеждает.
        Пользователь стреляет в комнату с мышью. Получает шум. Стрелы -=1
        Пользователь стреляет в комнату с пропастью. Получает потерю стрелы. Стрелы -=1
        Пользователь стреляет в пустую комнату. Стрелы -=-1.
        Если стрелы кончились, то Игра окончена.
        Услышав выстрел, вампус перемещается в соседнюю комнату.
        Если вампус оказыватся в комнате с игроком, игра окончена.       
        Пользователь в пустой комнате. Завершение действия.
        
        """



class Room():
    """
    Data-class for data about room
    
    """
    def __init__(self, room_number:int, next_room:set) -> None:
        self.room_number = room_number
        self.next_room = next_room
        self.deep = False
        self.bat = False
    

class Unit():
    """
    Неиспользуемый класс, при расширении функциональности, он него можно наследовать класс Player и класс Vampus

    """
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
    """
    Неиспользуемый класс. Здесь можно хранить состояние героя, а так же двигать его и стрелять, но проще оказалось все это
    оставить в основном классе игры.
    """
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


class Vampus(Unit):
    """
    Неиспользуемый класс для вампуса, возможно пригодится при расщирении функционала
    """
    def fear_arrow(self):
        if random.choice([1,2,3,4]) == 1:
           self.random_move()
    

class Logic():
    """ 
    Логику можно (было бы) переместить сюда, но пока она в методе Map.action()
    """
    pass