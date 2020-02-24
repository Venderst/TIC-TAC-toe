import os
import sys

from game_objects import CELL_STATES, GAME_RESULTS


def clear_screen():
    clear_command_names = {
        'linux': 'clear',
        'linux1': 'clear',
        'linux2': 'clear',
        'darwin': 'clear',
        'win32': 'cls'
    }
    os.system(clear_command_names.get(sys.platform, 'clear'))


class View(object):

    def __init__(self, is_drawing_available=True):
        self._is_drawing_available = is_drawing_available

    def enable_drawing(self):
        self._is_drawing_available = True

    def disable_drawing(self):
        self._is_drawing_available = False

    def draw(self, field: list):
        if not self._is_drawing_available:
            return
        clear_screen()
        for i in range(len(field)):
            row_str = ' '
            for j in range(len(field[i])):
                cell = field[i][j]
                if cell == CELL_STATES['zero']:
                    row_str += 'O|'
                elif cell == CELL_STATES['cross']:
                    row_str += 'X|'
                else:
                    row_str += ' |'
            print(row_str[:-1], end='\n')
            if i < len(field) - 1:
                print(' ' + '-' * 5, end='\n')

    def print_human_readable_game_result(self, game_result: int):
        if not self._is_drawing_available:
            return
        assert game_result in GAME_RESULTS.values(), 'Game result must be one of the GAME_RESULTS values'
        human_readable_game_results = {
            0: 'Nothing',
            1: 'Cross won',
            2: 'Zero won',
            3: 'Draw'
        }
        print(human_readable_game_results[game_result])
