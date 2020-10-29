import time
import SimWorld


SECONDS = 30                                   # Time Limit for backtracking to find solution (1 pin left)
best_score = 40                                # holds best result in pins backtracking achieved in SECONDS
NRUNS = 5                                      # run backtracking for n runs

""" Set Up Board to play on """
moves_to_victory = []
Brett1 = SimWorld.Diamond(6)
Brett1.populate_board()
Brett1.board_array[0][0].set_value(0)
# Brett1.board_array[5][5].set_value(0)
# Brett1.board_array[2][2].set_value(0)
# Brett1.board_array[2][3].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()


def solve_solitaer():
    """
    uses Backtracking to get a solution for the solitaer puzzle and saves the necessary moves in moves_to_victory
    """
    global best_score
    score = (Brett1.get_board_view() == 1).sum()
    if score < best_score:
        best_score = score

    if score == 1:  # and Brett1.board_array[5][5].get_value() == 1         #Ennglish board center condition
        return True
    if time.time() - start_time > SECONDS:
        return True
    else:
        posb_moves = Brett1.get_actions()
        for i in range(30):
            if len(posb_moves) == 0:
                return False
            previous_board = Brett1.get_board_copy()
            current_move = posb_moves[0]
            moves_to_victory.append(current_move)
            Brett1.take_action(posb_moves[0])
            if solve_solitaer() is True:
                return True
            posb_moves.pop(0)
            moves_to_victory.pop()  # pops last element
            Brett1.board_array = previous_board.copy()


avg = 0
for i in range(NRUNS):
    start_time = time.time()
    solve_solitaer()
    print(moves_to_victory)
    print(Brett1.get_board_view())
    print("Best score was", best_score)
    Brett1.board_array = start_board
    start_board = Brett1.get_board_copy()
    moves_to_victory.clear()
    avg += (time.time() - start_time) / NRUNS
    print("--- %s seconds ---" % (time.time() - start_time))

print("---")
print(avg)
print("---")
