from models import *
from controller import *

if __name__ == "__main__":
    map = Map()
    map.start_game()
    player = Player(arrows=7, map = map, life=1)
    controller = ConsolController()
    game_is_run = True
    controller.start_message()
 
    while game_is_run:

        this_room = map.players_room
        target = map.maze[this_room].next_room
        smell = map.get_smell(room=this_room)
        breeze = map.get_breeze(room=this_room)
        noize = map.get_noise(room=this_room)
        arrows =map.arrows

        controller.status_message(this_room, target, smell=smell, noise=noize, breeze=breeze, arrow=arrows)
        action = controller.ask_action(this_room, target)
        result = map.action(**action)
        controller.event_message(**result)
        
        #print('debag_info: ')
        #print (result)
        #print('bats: {}'.format(map.bats),
        # "\n", 'deeps: ', map.deeps, 'vampus: ', map.vampuses_room, "\n")

        #controller.event_message(result)
        if result['player_died']:
            print('Game over')
            #controller.lose()
            break
        if result['vampus_died']:
            print('You win! \nGame over')
            #controller.win()False
            break
        if result['no_arrows']:
            print('Game over')
            break

        