import os
from copy import deepcopy

from game_objects import CELL_STATES, GAME_RESULTS
from view import View
from world_updater import validate_transition, check_if_winning_field_state, check_if_draw_field_state

from models.human_model import HumanModel
from models.minimax_model import MiniMaxModel

MODELS_DATA_DIR = 'models_data'

if not os.path.exists(MODELS_DATA_DIR):
    os.mkdir(MODELS_DATA_DIR)

FIELD_WIDTH = 3
FIELD_HEIGHT = 3

view = View(True)

models = [MiniMaxModel(use_cached_actions=False), HumanModel()]
models[0].set_state(CELL_STATES['cross'])
models[1].set_state(CELL_STATES['zero'])

models[0].load(MODELS_DATA_DIR)
models[1].load(MODELS_DATA_DIR)

replays_num = -1
replay_index = 0
is_game_over = False

while (replay_index < replays_num and replays_num > 0) or replays_num < 1 and not is_game_over:
    field = [
        [CELL_STATES['empty'] for _ in range(FIELD_WIDTH)]
        for _ in range(FIELD_HEIGHT)
    ]

    view.draw(field)
    temp = models[0].get_state()
    models[0].set_state(models[1].get_state())
    models[1].set_state(temp)
    temp = deepcopy(models[0])
    models[0] = deepcopy(models[1])
    models[1] = temp

    game_result = GAME_RESULTS['NOTHING']

    while not game_result:
        cross_model_transition = models[0].make_turn(deepcopy(field))

        if not validate_transition(field, cross_model_transition):
            game_result = GAME_RESULTS['ZERO_WON']
            break
        else:
            field[cross_model_transition[0]][cross_model_transition[1]] = CELL_STATES['cross']
            if check_if_winning_field_state(field):
                game_result = GAME_RESULTS['CROSS_WON']
                break

        if check_if_draw_field_state(field):
            game_result = GAME_RESULTS['DRAW']
            break

        models[0].set_game_result(game_result, field)

        view.draw(field)

        zero_model_transition = models[1].make_turn(deepcopy(field))

        if not validate_transition(field, zero_model_transition):
            game_result = GAME_RESULTS['CROSS_WON']
            break
        else:
            field[zero_model_transition[0]][zero_model_transition[1]] = CELL_STATES['zero']
            if check_if_winning_field_state(field):
                game_result = GAME_RESULTS['ZERO_WON']
                break
        models[1].set_game_result(game_result, field)
        view.draw(field)

    models[0].set_game_result(game_result, field)
    models[1].set_game_result(game_result, field)

    view.draw(field)
    view.print_human_readable_game_result(game_result)
    user_answer = input('Do you want to continue? [y/n]')
    if user_answer.lower() != 'y':
        is_game_over = True

models[0].save(MODELS_DATA_DIR)
models[1].save(MODELS_DATA_DIR)
