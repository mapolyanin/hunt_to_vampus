"""This modul is main modul in 'Hunter to Vampus' game.

"""
import random

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
    """This is main class of game.
    Atributes
    ----------
    maze: set
        set objects Room
    deeps: list
        list for temporaly storage rooms with deep.
    bats: list
        list for temporaly storage rooms with bats.
    vampuses_room: int
        storage for position of Vampus.
    players_room: int
        storage fo position of Player.
    arrow: int:
        storage for arrow.
    Methods
    -------
    __init__()
        create object Maze

    start_game():
        create maze from GRAF, take and storage position for Vampus, bats,
        deep and Player.

    get_smell(room:int) -> bool
    get_noise(room:int) -> bool
    get_breeze(room:int) -> bool

        get info about deeps, bats and Vampus in next room.

    action(fire:bool, move:bool, target:int)
        reaction game on action of Player
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
        #set vampus position
        self.vampuses_room = random.choice(list(_unused_rooms))
        _unused_rooms.discard(self.vampuses_room)

        for i in range(0, BATS):
            #set bats position
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

    def get_state(self):
        """This method return state of game before Players something do. """

        this_room = self.players_room
        target = self.maze[self.players_room].next_room
        smell = self.get_smell(self.players_room)
        noise = self.get_noise(self.players_room)
        breeze = self.get_breeze(self.players_room)
        return {'room': self.players_room, 'target':target, 'smell':smell, 'noise':noise, 'breeze':breeze, 'arrow':self.arrows}
        pass

    def get_breeze(self, room:int) -> bool:
        """
        Call this metod for feel breeze... from deep
        """
        for i in self.maze[room].next_room:
            if self.maze[i].deep:
                return True
        return False


    def get_noise(self, room):
        """
        Call this metod to hear the noize from bat
        """
        for i in self.maze[room].next_room:
            if self.maze[i].bat:
                return True
        return False

    def action(self, fire:bool, move:bool, target:int):
        """
        This metod return result of users action.


        """

        #this stait after action
        result = {'vampus_died':False,
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
            result['bat_transfer'] = new_room.room_number

        if self.players_room == self.vampuses_room:
            result['player_meet_vampus'] = True
            result['player_died'] = True

        if self.maze[self.players_room].deep:
            #player is died in deep
            result['deep'] = True
            result['player_died'] = True
            result['lose'] = True

        if fire:
            #if player fired
            self.arrows -=1
            if target == self.vampuses_room:
                #we died vampus!
                result ['vampus_died'] = True
                result['win'] = True
            elif self.maze[target].bat:
                #bat detect in target room
                result ['bat_detect']= True
            elif self.maze[target].deep:
                #deep detect in target room
                result ['deep_detect']=True
            else:
                #empty room
                result['empty_room']=True

            #vampus wake up after fire...may be
            if (random.choice(range(0,4)) in [0,1] and not result['vampus_died']):
                result['vampus_fear'] = True
                #перемещаем вампуса в соседнюю комнату. Если там мыши или пропасть,
                #он там спать не будет, и пойдет дальше.
                while True:
                    new_room = random.choice(list(self.maze[self.vampuses_room].next_room))
                    self.vampuses_room = new_room
                    if (self.maze[self.vampuses_room].bat or self.maze[self.vampuses_room].deep):
                        continue
                    else:
                        break
                if self.vampuses_room == self.players_room:
                    #player is tourist breakfast for vampus
                    result['vampus_meet_player'] = True
                    result['player_died'] = True
                    result['lose'] = True


        if self.arrows == 0:
            #if arrows is out, game is over

            result['no_arrows'] = True
            result['lose'] = True
        return result

class Room():
    """
    Data-class for data about room

    """
    def __init__(self, room_number:int, next_room:set) -> None:
        self.room_number = room_number
        self.next_room = next_room
        self.deep = False
        self.bat = False
