from controller import *
from models import *
import pytest

map = Map()
map.start_game()
controller = ConsolController()

def test_start_message():
    assert controller.start_message()== None


def test_status_message():
    for i in range(1, 21):
        controller.status_message(i, map.maze[i].next_room,
        map.get_smell(i), map.get_noise(i), map.get_breeze(i))

def test_ask_action():
    return controller.ask_action(1, {2, 5, 6})


if __name__ == "__main__":
    print(test_ask_action())