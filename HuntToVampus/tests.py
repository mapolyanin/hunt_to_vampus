from pymacaroons import MACAROON_V1
from models import *
def graf_test():
    for i in GRAF:
        for k in GRAF[i]:
            assert i in GRAF[k]
        
def test_Map():
    map = Map()
    assert map.start_game() == None
    print (map.bats)
    print (map.deeps)
    print(map.players_room)
    print(map.vampuses_room)


if (__name__ == "__main__"):
    graf_test()
    test_Map()