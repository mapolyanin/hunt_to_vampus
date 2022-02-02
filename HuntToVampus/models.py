"""This module is main module in 'Hunter to wumpus' game.

"""
import random

# map of game.
GRAPH = {
    1: {2, 5, 6},  # a
    2: {1, 8, 3},  # b
    3: {2, 4, 10},  # c
    4: {3, 5, 12},  # d
    5: {4, 1, 14},  # e
    6: {1, 7, 15},  # f
    7: {6, 8, 16},  # g
    8: {7, 9, 2},  # h
    9: {8, 10, 17},  # i
    10: {9, 11, 3},  # j
    11: {10, 12, 18},  # k
    12: {11, 13, 4},  # l
    13: {12, 14, 19},  # m
    14: {13, 15, 5},  # n
    15: {14, 6, 20},  # o
    16: {20, 17, 7},  # p
    17: {16, 18, 9},  # q
    18: {17, 19, 11},  # r
    19: {18, 20, 13},  # s
    20: {19, 16, 15},  # t
}
LIFE = 1
ARROWS = 7
BATS = 2
DEEPS = 2
#random.seed(1000)  # comment this after debugging and refactoring


class Map:
    """This is main class of game.
    Attributes
    ----------
    maze: set
        objects Room
    deeps: list
        for temporally storage rooms with deep.
    bats: list
        for temporally storage rooms with bats.
    wumpus_room: int
        storage for position of wumpus.
    players_room: int
        storage fo position of Player.
    arrows: int:
        storage for arrow.
    Methods
    -------
    __init__()
        create object Maze

    start_game():
        create maze from GRAPH, take and storage position for wumpus, bats,
        deep and Player.

    get_smell(room:int) -> bool
    get_noise(room:int) -> bool
    get_breeze(room:int) -> bool

        get info about deeps, bats and wumpus in next room.

    action(fire:bool, move:bool, target:int)
        reaction game on action of Player
    """

    def __init__(self):
        self.maze = dict()
        self.deeps = []
        self.bats = []
        self.wumpus_room = None
        self.players_room = None
        self.arrows = ARROWS

    def start_game(self):
        """
        this method must be called before game
        """
        _unused_rooms = set(GRAPH.keys())
        # set wumpus position
        self.wumpus_room = random.choice(list(_unused_rooms))
        _unused_rooms.discard(self.wumpus_room)

        for i in range(0, BATS):
            # set bats position
            room = random.choice(list(_unused_rooms))
            self.bats.append(room)
            _unused_rooms.discard(room)

        # set deeps
        for i in range(0, DEEPS):
            room = random.choice(list(_unused_rooms))
            self.deeps.append(room)
            _unused_rooms.discard(room)

        # set player in room, where not wumpus, bats, deeps, and bad neighbors ))
        _used_rooms = set(GRAPH.keys()).difference(_unused_rooms)

        for i in _used_rooms:
            for k in GRAPH[i]:
                _unused_rooms.discard(k)

        self.players_room = random.choice(list(_unused_rooms))

        for i in GRAPH.keys():
            self.maze[i] = Room(room_number=i,
                                next_room=GRAPH[i])

        for i in self.deeps:
            self.maze[i].deep = True

        for i in self.bats:
            self.maze[i].bat = True

    def get_smell(self, room: int) -> bool:
        """
        Call this method for smelled wumpus
        """

        for i in self.maze[room].next_room:
            if i == self.wumpus_room:
                return True
        return False

    def get_state(self):
        """This method return state of game before Players something do. """

        target = self.maze[self.players_room].next_room
        smell = self.get_smell(self.players_room)
        noise = self.get_noise(self.players_room)
        breeze = self.get_breeze(self.players_room)
        return {'room': self.players_room, 'target': target, 'smell': smell, 'noise': noise, 'breeze': breeze,
                'arrow': self.arrows}
        pass

    def get_breeze(self, room: int) -> bool:
        """
        Call this method for feel breeze... from deep
        """
        for i in self.maze[room].next_room:
            if self.maze[i].deep:
                return True
        return False

    def get_noise(self, room):
        """
        Call this method to hear the noize from bat
        """
        for i in self.maze[room].next_room:
            if self.maze[i].bat:
                return True
        return False

    def action(self, fire: bool, move: bool, target: int):
        """
        This method return result of users action.


        """

        # this state after action
        result = {'wumpus_died': False,
                  'player_died': False,
                  'win': False,
                  'lose': False,
                  'bat_detect': False,
                  'deep_detect': False,
                  'empty_room': False,
                  'bat_transfer': 0,
                  'player_meet_wumpus': False,
                  'wumpus_meet_player': False,
                  'deep': False,
                  'no_arrows': False,
                  'wumpus_fear': False
                  }

        # validated
        if fire ^ move:
            pass
        else:
            return None

        if target in self.maze[self.players_room].next_room:
            pass
        else:
            return None

        if move:
            # move_player in next room
            self.players_room = target
        if self.maze[self.players_room].bat:
            # action, if in new room live bat
            while True:
                new_room = random.choice(self.maze)
                if new_room.bat:
                    continue
                else:
                    self.players_room = new_room.room_number
                    break
            result['bat_transfer'] = new_room.room_number

        if self.players_room == self.wumpus_room:
            result['player_meet_wumpus'] = True
            result['player_died'] = True

        if self.maze[self.players_room].deep:
            # player is died in deep
            result['deep'] = True
            result['player_died'] = True
            result['lose'] = True

        if fire:
            # if player fired
            self.arrows -= 1
            if target == self.wumpus_room:
                # we died wumpus!
                result['wumpus_died'] = True
                result['win'] = True
            elif self.maze[target].bat:
                # bat detect in target room
                result['bat_detect'] = True
            elif self.maze[target].deep:
                # deep detect in target room
                result['deep_detect'] = True
            else:
                # empty room
                result['empty_room'] = True

            # wumpus wake up after fire...may be
            if random.choice(range(0, 4)) in [0, 1] and not result['wumpus_died']:
                result['wumpus_fear'] = True

                while True:
                    new_room = random.choice(list(self.maze[self.wumpus_room].next_room))
                    self.wumpus_room = new_room
                    if self.maze[self.wumpus_room].bat or self.maze[self.wumpus_room].deep:
                        continue
                    else:
                        break
                if self.wumpus_room == self.players_room:
                    # player is tourist breakfast for wumpus
                    result['wumpus_meet_player'] = True
                    result['player_died'] = True
                    result['lose'] = True

        if self.arrows == 0:
            # if arrows is out, game is over

            result['no_arrows'] = True
            result['lose'] = True
        return result


class Room:
    """
    Storage for data about room.

    """

    def __init__(self, room_number: int, next_room: set) -> None:
        self.room_number = room_number
        self.next_room = next_room
        self.deep = False
        self.bat = False
