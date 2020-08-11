import solit_random
import numpy as np
import random

def evaluate_bord(board):
    """
    compare policy with pins on board to calculate value of the state:

    example evaluation, "value-function" replace with updating value function later.
    """
    policy_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, -1, -2, -1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
                              [0, 0,-2, 0, 0, 1, 0, 0, -2, 0, 0],
                             [0, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, -1, -2, -1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    return np.sum(np.multiply(board, policy_board))


def policy_move():
    """
    looks at the board after each possible move and then chooses the move that leaves the most options for the next move
    seems to work fine
    """
    list_of_values = []
    current_board = solit_random.board.copy()
    valid_m = solit_random.find_valid_moves()
    if len(valid_m) == 0:  # return 0 if there is no valid move
        return 0
    for element in range(len(valid_m)):  # perform valid moves, then add length of the now possible moves to list
        next_move = valid_m[element]
        solit_random.move(next_move[0], next_move[1])
        list_of_values.append(evaluate_bord(solit_random.board))
        solit_random.board = current_board.copy()

    m = max(list_of_values)
    favoured_move_index = list_of_values.index(m)
    favoured_move = valid_m[favoured_move_index]
    solit_random.move(favoured_move[0], favoured_move[1])
    return 1

def policy_move_2():
    """
    looks two moves ahead and then chooses the move that leaves the most options for the next move

    """
    list_of_scored_moves = []
    current_board = solit_random.board.copy()
    valid_m = solit_random.find_valid_moves()
    if len(valid_m) == 0:  # return 0 if there is no valid move
        return 0
    for element in range(len(valid_m)):  # make each possible move
        next_move = valid_m[element]
        solit_random.move(next_move[0], next_move[1])
        list_after = solit_random.find_valid_moves()
        if len(list_after) == 0:  # if there are no more possible moves, look ahead with depth 1 and make a move
            solit_random.board = current_board.copy()
            return policy_move()
        for element2 in range(len(list_after)):  # make a possible move, then
            next_move_2 = list_after[element2]
            solit_random.move(next_move_2[0], next_move_2[1])

            list_after_2 = solit_random.find_valid_moves()  # append index + valuescore
            list_of_scored_moves.append([element, evaluate_bord(solit_random.board)])
    solit_random.board = current_board.copy()
    indices, list_of_values = zip(*list_of_scored_moves)
    m = max(list_of_values)
    favoured_move_index = indices[list_of_values.index(m)]
    favoured_move = valid_m[favoured_move_index]
    solit_random.move(favoured_move[0], favoured_move[1])
    solit_random.move(favoured_move[0], favoured_move[1])
    return 1