from models import *
from controller import *


def graf_test():
    for i in GRAF:
        for k in GRAF[i]:
            assert i in GRAF[k]
        
def test_Map(map):
    
    assert map.start_game() == None
    print (map.bats)
    print (map.deeps)
    print(map.players_room)
    print(map.vampuses_room)

    
    assert (map.get_smell(5) == True)

    assert (map.get_smell(1)== False)





if (__name__ == "__main__"):
    map = Map()
    graf_test()
    test_Map(map)
    player = Player(5, map, 1)
    print(replic['room'].format("1"))
    print(replic['bat'].format('3'))
    print(map.maze[18].next_room)
    target = map.maze[1].next_room
    print(target)


