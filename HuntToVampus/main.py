from models import *
from controller import *

if __name__ == "__main__":
    map = Map()
    player = Player(arrows=7, map = map, life=1)
    while True:
        if player.life == 0:
            break
        pass