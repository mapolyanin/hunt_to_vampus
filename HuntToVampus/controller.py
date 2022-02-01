"""This is controller module.

Now in this module only consol controller and Russian. New controllers coming soon.
Text imported from  lang/*.json
"""
import json

with open("lang/ru-ru.json", 'r', encoding='utf-8') as file:
    ru_replics = json.load(file)
    replic = ru_replics


class ConsolController():
    """Class for console gamind in Hunt to Vampus"""

    def start_message(self):
        """Print start message of game"""
        print(replic["start"])


    def status_message(self, room:int, target:set,
                       smell:bool, noise:bool,
                       breeze:bool, arrow:int):
        """Method for printing status message"""

        print(replic['room'].format(room))
        print(replic['next_room'].format(target))
        print(replic['arrow_limit'].format(arrow))

        if smell:
            print (replic['smell'])
        if noise:
            print(replic['noise'])
        if breeze:
            print(replic['breeze'])
        print('\n')

    def ask_action(self, target:set) -> dict:
        """Method for input from Player"""
        move = False
        fire = False
        self.target = None

        while not(move or fire):

            _action = input(replic['action_ask']).lower()
            if _action in {'m', 'м'}:
                move = True

            elif _action in {'f'}:
                fire = True
            else:
                print(replic['wrong_answer'])

        while True:
            if move:
                print(replic['move_ask'])
            elif fire:
                print(replic['fire_ask'])

            _target = input(replic['say_room'])

            if _target.isdigit():
                if int(_target) in target:
                    self.target = int(_target)
                    break
                else:
                    print(replic['wrong_answer'])

            else:
                print(replic['wrong_answer'])
                continue

        return {"move": move, "fire": fire, "target":self.target}

    def event_message(self, **kwards):
        """Print reaction of game on Player"""

        if kwards['vampus_died']:
            print(replic['vampus_died'])

        if kwards['win']:
            print(replic['win'])

        if kwards['bat_detect']:
            print(replic['arrow_and_bat'])

        if kwards['deep_detect']:
            print(replic['arrow_down'])

        if kwards['empty_room']:
            print(replic["empty_room"])

        if kwards['vampus_fear']:
            print(replic['vampus_move'])

        if kwards['bat_transfer']:
            print(replic["bat"].format(kwards['bat_transfer']))

        if (kwards['bat_transfer'] and kwards['deep']):
            print(replic['bat_and_deep'])
            print(replic['lose'])

        if kwards['player_meet_vampus']:
            print(replic["you_move_in_vampuses_room"])
            print(replic['lose'])

        if kwards['vampus_meet_player']:
            print(replic["vampus_move_in_your_room"])
            print(replic['lose'])

        if kwards['deep']:
            print(replic["deep"])
            print(replic['lose'])

        if kwards['no_arrows']:
            print(replic["no_arrows"])
            print(replic["lose"])
