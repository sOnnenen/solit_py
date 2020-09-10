import random
import time
import SimWorld

moves_to_victory = []
Brett1 = SimWorld.Diamond(5)
Brett1.populate_board()
# Brett1.board_array[5][5].set_value(0)
# Brett1.board_array[0][0].set_value(0)
Brett1.board_array[2][2].set_value(0)
#Brett1.board_array[2][3].set_value(0)
Brett1.set_neighbor_pairs()
print(Brett1.get_board_view())
start_board = Brett1.get_board_copy()


def solve_solitaer():
    """
    uses Backtracking to get a solution for the solitaer puzzle and saves the necessary moves in moves_to_victory
    """
    #  Analog zu N-Damen Problem https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/
    #  https://www.youtube.com/watch?v=0DeznFqrgAI
    if(Brett1.get_board_view() == 1).sum() == 2:  # and solit_random.board[5][5] == 2
        return True
    else:
        posb_moves = Brett1.get_actions();
        for i in range(30):
            if len(posb_moves) == 0:
                return False
            previous_board = Brett1.get_board_copy()
            r = randomtable[len(posb_moves)-1]
            current_move = posb_moves[r]                            # random.randint(0, len(posb_moves)) instead of 0
            # current_move = posb_moves[0]
            moves_to_victory.append(current_move)
            Brett1.take_action(posb_moves[r])
            if solve_solitaer() is True:
                return True
            # print(posb_moves)
            # bla = [*posb_moves]
            # bla.pop(r)
            # posb_moves = (tuple(bla),)  # pops first element of list, for higher performance look at collections.deq
            posb_moves.pop(r)
            # print(posb_moves)
            moves_to_victory.pop()  # pops last element
            # print(Brett1.get_board_view())
            Brett1.board_array = previous_board.copy()

avg = 0
nruns = 5
for i in range(nruns):
    randomtable = [random.randint(0, i) for i in range(50)]
    print(randomtable)
    start_time = time.time()
    solve_solitaer()
    print(moves_to_victory)
    print(Brett1.get_board_view())
    Brett1.board_array = start_board
    start_board = Brett1.get_board_copy()
    moves_to_victory.clear()
    avg += (time.time() - start_time)/nruns
    print("--- %s seconds ---" % (time.time() - start_time))
print("---")
print(avg)
print("---")