"""Start module. Jast type: python3 main.py"""

from models import Map
from controller import ConsolController

if __name__ == "__main__":
    game_map = Map()
    game_map.start_game()
    controller = ConsolController()
    game_is_run = True
    controller.start_message()

    while game_is_run:
        #get state of game
        # this_room = game_map.players_room
        # target = game_map.maze[this_room].next_room
        # smell = game_map.get_smell(room=this_room)
        # breeze = game_map.get_breeze(room=this_room)
        # noize = game_map.get_noise(room=this_room)
        # arrows =game_map.arrows
        state = game_map.get_state()
        controller.status_message(**state)
        # controller.status_message(this_room, target, smell=smell,
        # noise=noize, breeze=breeze, arrow=arrows)
        action = controller.ask_action(state['target'])
        result = game_map.action(**action)
        controller.event_message(**result)

        if result['player_died']:
            print('Game over')
            #controller.lose()
            game_is_run = False
        if result['vampus_died']:
            print('You win! \nGame over')
            #controller.win()False
            game_is_run = False
        if result['no_arrows']:
            print('Game over')
            game_is_run = False
