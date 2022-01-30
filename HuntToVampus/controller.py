
import json
ru_replics = json.load(open("lang/ru-ru.json"))
#ru_lang = json.loads(ru_json)
replic = ru_replics


class ConsolController():
    def start_message(self):
        print(replic["start"])
        pass

    def game_over_message(self):
        pass

    def status_message(self, room:int, target:set,
                       smell:bool, noise:bool, 
                       breeze:bool):
        print(replic['room'].format(room))
        print(replic['next_room'].format(target))
        if smell:
            print (replic['smell'])
        if noise:
            print(replic['noise'])
        if breeze:
            print(replic['breeze'])
        print('\n')

    def ask_action(self, room, target) -> dict:
        move = False
        fire = False
        self.target = None

        while not(move or fire):

            _action = input(replic['action_ask']).lower
            if _action in {'m', 'м'}:
                move = True
            elif _action in {'f'}:
                fire = True
            else:
                print(replic['wrong_answer'])
        if move == True:
            while True:
                _target = input(replic['move_ask']).lower
                if is+* _target



            



        return {"move": move, "fire": fire, "target":target}
            





    def ask_move(self, room, target):
        pass

    def ask_fire(self, room, target):
        pass

    def event_message(self):
        pass

    def lose():
        pass

    def win():
        print(replic["win"])
        