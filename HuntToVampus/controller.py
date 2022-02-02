"""This is controller module.

Now in this module only consol controller and Russian. New controllers coming soon.
Text imported from  lang/*.json
"""
import json

with open("lang/ru-ru.json", 'r', encoding='utf-8') as file:
    ru_replicas = json.load(file)
    replicas = ru_replicas


class ConsoleController:
    """Class for console gamind in Hunt to wumpus"""
    @staticmethod
    def start_message():
        """Print start message of game"""
        print(replicas["start"])
        print('\n')

    def status_message(self, room:int, target:set,
                       smell:bool, noise:bool,
                       breeze:bool, arrow:int):
        """Method for printing status message"""

        print(replicas['room'].format(room))
        print(replicas['next_room'].format(target))
        print(replicas['arrow_limit'].format(arrow))

        if smell:
            print(replicas['smell'])
        if noise:
            print(replicas['noise'])
        if breeze:
            print(replicas['breeze'])
        print('\n')

    def ask_action(self, target:set) -> dict:
        """Method for input from Player"""
        move = False
        fire = False
        self.target = None

        while not(move or fire):

            _action = input(replicas['action_ask']).lower()
            if _action in {'m', 'м'}:
                move = True

            elif _action in {'f'}:
                fire = True
            else:
                print(replicas['wrong_answer'])

        while True:
            if move:
                print(replicas['move_ask'])
            elif fire:
                print(replicas['fire_ask'])

            _target = input(replicas['say_room'])

            if _target.isdigit():
                if int(_target) in target:
                    self.target = int(_target)
                    break
                else:
                    print(replicas['wrong_answer'])

            else:
                print(replicas['wrong_answer'])
                continue

        return {"move": move, "fire": fire, "target":self.target}

    @staticmethod
    def event_message(**kwards):
        """Print reaction of game on Player"""
        print('\n')
        if kwards['wumpus_died']:
            print(replicas['wumpus_died'])

        if kwards['win']:
            print(replicas['win'])

        if kwards['bat_detect']:
            print(replicas['arrow_and_bat'])

        if kwards['deep_detect']:
            print(replicas['arrow_down'])

        if kwards['empty_room']:
            print(replicas["empty_room"])

        if kwards['wumpus_fear']:
            print(replicas['wumpus_move'])

        if kwards['bat_transfer']:
            print(replicas["bat"].format(kwards['bat_transfer']))

        if kwards['bat_transfer'] and kwards['deep']:
            print(replicas['bat_and_deep'])
            print(replicas['lose'])

        if kwards['player_meet_wumpus']:
            print(replicas["you_move_in_wumpuses_room"])
            print(replicas['lose'])

        if kwards['wumpus_meet_player']:
            print(replicas["wumpus_move_in_your_room"])
            print(replicas['lose'])

        if kwards['deep']:
            print(replicas["deep"])
            print(replicas['lose'])

        if kwards['no_arrows']:
            print(replicas["no_arrows"])
            print(replicas["lose"])
        print('\n')
