import solit_random
import numpy as np

list_of_states = [solit_random.start_board]


def positions_n_jumps(depth, board):
    for n in range(depth):
        posb_moves = solit_random.find_valid_moves()
        for i in range(len(posb_moves)):
            previous_board = solit_random.board.copy()
            current_move = posb_moves[i]
            solit_random.move(current_move[0], current_move[1])
            board_in_list = False
            for element in range(len(list_of_states)):
                if compare_boards(list_of_states[element].copy(), solit_random.board.copy()):
                    board_in_list = True
                    break
            if(board_in_list is True):
                if i < len(posb_moves)-1:
                    solit_random.board = previous_board.copy()
            else:
                list_of_states.append(solit_random.board.copy())
                positions_n_jumps(depth - n-1, solit_random.board.copy())
                solit_random.board = previous_board.copy()


def compare_boards(board1, board2):
    board1t = board1.transpose()
    if (board1 == board2).all():
        return True
    rot1 = np.rot90(board2)
    if(board1 == rot1).all():
        return True
    rot2 = np.rot90(rot1)
    if (board1 == rot2).all():
        return True
    rot3 = np.rot90(rot2)
    if (board1 == rot3).all():
        return True
    if (board1t == board2).all():
        return True
    if(board1t == rot1).all():
        return True
    if (board1t == rot2).all():
        return True
    if (board1t == rot3).all():
        return True

    return False


print("Count all the possible board positions up to a depth of n moves (not counting symmetric positions)")
print("Depth 6 should take ~ 1 minute, Depth 7 takes ~27minutes")
depth = int(input("Enter a depth n:  n = "))
positions_n_jumps(depth,solit_random.start_board.copy())

'''
# Displays 

empty3 = 0
empty4 = 0
empty5 = 0
empty6 = 0
empty7 = 0

for element in range(len(list_of_states)):
    if (list_of_states[element]==1).sum() == 3:
        empty3 += 1
    if (list_of_states[element]==1).sum() == 4:
        empty4 += 1
    if (list_of_states[element] == 1).sum() == 5:
            empty5 += 1
    if (list_of_states[element] == 1).sum() == 6:
        empty6 += 1
    if (list_of_states[element] == 1).sum() == 7:
        empty7 += 1
    if (list_of_states[element] == 1).sum() == 8:
        empty8 += 1
    if (list_of_states[element] == 1).sum() == 9:
        empty9 += 1
print("After ", depth,  " moves, we have ", len(list_of_states), " possible states")
print("30 Pegs x", empty3, "29 Pegs x", empty4, "28 Pegs x", empty5, "27 Pegs x", empty6, "26 Pegs x", empty7, "25 Pegs x")
#  count how many with x 2s(Pegs) are left

'''
print("After ", depth,  " moves, we have ", len(list_of_states), " possible states")

