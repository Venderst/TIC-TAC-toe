from game_objects import CELL_STATES


def validate_transition(field, transition: tuple) -> bool:
    # transition in a new position (row, col) of player state
    if not transition:
        return False
    if 0 <= transition[0] <= len(field) and 0 <= transition[1] <= len(field[0]):
        return field[transition[0]][transition[1]] == CELL_STATES['empty']


def check_if_winning_field_state(field):
    # diagonals
    result = field[0][0] == field[1][1] == field[2][2] and field[0][0]
    result = result or field[0][2] == field[1][1] == field[2][0] and field[0][2]

    # rows
    result = result or field[0][0] == field[0][1] == field[0][2] and field[0][0]
    result = result or field[1][0] == field[1][1] == field[1][2] and field[1][0]
    result = result or field[2][0] == field[2][1] == field[2][2] and field[2][0]

    # cols
    result = result or field[0][0] == field[1][0] == field[2][0] and field[0][0]
    result = result or field[0][1] == field[1][1] == field[2][1] and field[0][1]
    result = result or field[0][2] == field[1][2] == field[2][2] and field[0][2]

    return result


def check_if_draw_field_state(field):
    return all([all(row) for row in field])
