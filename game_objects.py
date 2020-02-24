from abc import ABC, abstractmethod


CELL_STATES = {
    'empty': 0,
    'cross': 1,
    'zero': 2
}

GAME_RESULTS = {
    'NOTHING': 0,
    'CROSS_WON': 1,
    'ZERO_WON': 2,
    'DRAW': 3
}


class Model(ABC):

    def __init__(self):
        self._state = None

    def load(self, model_data_dir='models_data'):
        pass

    def save(self, model_data_dir='models_data'):
        pass

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    @abstractmethod
    def make_turn(self, field):
        pass

    def set_game_result(self, game_result, new_field):
        pass
