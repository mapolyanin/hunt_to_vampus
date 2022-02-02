"""Start module. Jast type: python3 main.py"""

from models import Map
from controller import ConsoleController

if __name__ == "__main__":
    game_map = Map()
    game_map.start_game()
    controller = ConsoleController()
    game_is_run = True
    controller.start_message()

    while game_is_run:
        state = game_map.get_state()
        controller.status_message(**state)
        action = controller.ask_action(state['target'])
        result = game_map.action(**action)
        controller.event_message(**result)

        if result['player_died']:
            print('Game over')
            game_is_run = False
        if result['wumpus_died']:
            print('You win! \nGame over')
            game_is_run = False
        if result['no_arrows']:
            print('Game over')
            game_is_run = False
