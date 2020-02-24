from game_objects import Model, CELL_STATES


class HumanModel(Model):

    def __init__(self):
        """
        The model required to enable human play
        """
        super().__init__()
        self._state = None
        self._state_symbol = ''

    def set_state(self, state):
        super().set_state(state)
        self._state_symbol = 'X' if state == CELL_STATES['cross'] else 'O'

    def make_turn(self, field):
        position = input(f'({self._state_symbol}) Your turn <row, col>:').replace(',', ' ')
        y, x = position.split()
        return int(y), int(x)
