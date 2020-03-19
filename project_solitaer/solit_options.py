import solit_random
import random


def make_move():
    """
    looks at the board after each possible move and then chooses the move that leaves the most options for the next move
    seems to work fine
    """
    list_of_length = []
    current_board = solit_random.board.copy()
    valid_m = solit_random.find_valid_moves()
    if len(valid_m) == 0:  # return 0 if there is no valid move
        return 0
    for element in range(len(valid_m)):  # perform valid moves, then add length of the now possible moves to list
        next_move = valid_m[element]
        solit_random.move(next_move[0], next_move[1])
        list_after = solit_random.find_valid_moves()
        list_of_length.append(len(list_after))
        solit_random.board = current_board.copy()
    m = max(list_of_length)  # look for the move that leaves the most possibilities and execute it
    list_of_max_options = [index for index, element in enumerate(list_of_length) if element == m]
    favoured_move_index = random.randint(0, len(list_of_max_options) - 1)
    favoured_move = valid_m[favoured_move_index]
    solit_random.move(favoured_move[0], favoured_move[1])
    return 1


def make_move_2():
    """
    looks two moves ahead and then chooses the move that leaves the most options for the next move
    still in beta
    """
    list_of_length = []
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
            return make_move()
        for element2 in range(len(list_after)):  # make a possible move, then
            next_move_2 = list_after[element2]
            solit_random.move(next_move_2[0], next_move_2[1])
            list_after_2 = solit_random.find_valid_moves()  # append index + amount of possible moves after the move
            list_of_length.append([element, len(list_after_2)])
    solit_random.board = current_board.copy()
    indices, lengths = zip(*list_of_length)
    m = max(lengths)  # look for the move that leaves the most possibilities and execute it
    list_of_max_options = [index for index, element in enumerate(lengths) if element == m]
    favoured_move_index = random.randint(0, len(list_of_max_options) - 1)
    favoured_move = valid_m[indices[favoured_move_index]]
    solit_random.move(favoured_move[0], favoured_move[1])
    return 1

