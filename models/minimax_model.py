import os
import json

import numpy as np

from game_objects import Model, CELL_STATES
from world_updater import check_if_winning_field_state, check_if_draw_field_state


class MiniMaxModel(Model):

    def __init__(self, use_cached_actions=True):
        """
        Recursive minimax model
        :param use_cached_actions: If False, one of the best actions is randomly
        selected each time. For low-power computers True is recommended
        """
        super().__init__()
        self._state = None
        self._use_cached_actions = use_cached_actions
        self._available_actions = dict()
        self._best_actions = dict()

    def load(self, model_data_dir='models_data'):
        data_file_path = os.path.join(model_data_dir, 'minimax_model_data.json')
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r') as file:
                loaded_data = json.load(file)
                self._available_actions = loaded_data.get('available_actions', dict())
                self._best_actions = loaded_data.get('best_actions', dict())

    def save(self, model_data_dir='models_data'):
        data_file_path = os.path.join(model_data_dir, 'minimax_model_data.json')
        saved_data = {
            'available_actions': self._available_actions,
            'best_actions': self._best_actions
        }
        with open(data_file_path, 'w') as file:
            json.dump(saved_data, file)

    def make_turn(self, field):
        field_hash = self._get_field_hash(field)
        if self._use_cached_actions and field_hash in self._best_actions:
            return self._best_actions[field_hash]
        action = self._eval_field(field, self._state)[1]
        action = (action // 3, action % 3)
        self._best_actions[field_hash] = action
        return action

    def _eval_field(self, field, player_state, action_index=0):
        if player_state == self._state:
            result = np.full_like(field, -100, dtype=np.float16)
        else:
            result = np.full_like(field, 100, dtype=np.float16)
        for i, j in self._get_available_positions(field):
            field[i][j] = player_state
            if check_if_winning_field_state(field):
                if player_state == self._state:
                    result[i][j] = 10
                else:
                    result[i][j] = -10
            elif check_if_draw_field_state(field):
                result[i][j] = 0
            else:
                result[i][j] = self._eval_field(
                    field, CELL_STATES['cross'] + CELL_STATES['zero'] - player_state, action_index + 1
                )[0]
            field[i][j] = CELL_STATES['empty']
        if player_state == self._state:
            return np.max(result), self._select_best_action(result)
        else:
            return np.min(result), self._select_best_action(result)

    @staticmethod
    def _select_best_action(evaluated_field: np.ndarray) -> int:
        available_indexes = np.where(evaluated_field == np.max(evaluated_field))
        selected_index = np.random.randint(len(available_indexes[0]))
        result = available_indexes[0][selected_index] * 3 + available_indexes[1][selected_index]
        return int(result)

    def _get_available_positions(self, field):
        field_hash = self._get_field_hash(field)
        result = self._available_actions.get(field_hash, None)
        if result is None:
            result = []
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == CELL_STATES['empty']:
                        result.append((i, j))
            self._available_actions[field_hash] = result
        return result

    @staticmethod
    def _get_field_hash(field):
        flat_field = np.ravel(field)
        multiplier = np.full(len(flat_field), 3) ** np.arange(len(flat_field))
        return str(np.sum(flat_field * multiplier))
