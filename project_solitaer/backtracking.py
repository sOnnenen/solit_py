import time
import SimWorld


SECONDS = 10                                                    # Zeitlimit um geforderte Pins zu erreichen
best_score = 40                                                 # Speichert den zwischenzeitlich besten erreichten Wert
NRUNS = 2                                                       # Anzahl der Anläufe
rint = 1                                                        # rintten zug nehmen wenn möglich
depth_limit = 33                                                # muss größer anzahl der züge bis zum ziel sein

""" Brett aufsetzen """
list_moves_to_victory = [[] for x in range(NRUNS)]
Brett1 = SimWorld.Diamond(6)
Brett1.populate_board()
Brett1.board_array[0][0].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()


def solve_solitaer(moves_to_victory):
    """
    backtracking algorithmus
    """
    global rint
    global best_score
    score = (Brett1.get_board_view() == 1).sum()
    if score < best_score:                                      # bestes Ergebnis setzen
        best_score = score

    if score == 1:  # and Brett1.board_array[5][5].get_value() == 1  # für englisches Brett Pin in Mitte
        return True
    if time.time() - start_time > SECONDS:                      # Zeitlimit prüfen
        return True
    else:
        posb_moves = Brett1.get_actions()
        for j in range(depth_limit):                            # kann depth limit züge zurückspringen
            if len(posb_moves) == 0:
                return False
            previous_board = Brett1.get_board_copy()
            current_move = 0
            if len(posb_moves) > rint:
                current_move = posb_moves[rint]
            else:
                current_move = posb_moves[0]
            moves_to_victory.append(current_move)
            Brett1.take_action(current_move)
            if solve_solitaer(moves_to_victory) is True:        # rekursion
                return True
            if len(posb_moves) > rint:
                posb_moves.pop(rint)
            else:
                posb_moves.pop(0)
            moves_to_victory.pop()                              # letztes element der liste entfernen
            Brett1.board_array = previous_board.copy()


avg = 0
list_of_scores = []
for i in range(NRUNS):
    rint = i+1
    start_time = time.time()
    solve_solitaer(list_moves_to_victory[i])
    print(list_moves_to_victory[i])
    print(Brett1.get_board_view())
    print("Best score was", best_score)
    Brett1.board_array = start_board
    start_board = Brett1.get_board_copy()
    best_score = 40
    avg += (time.time() - start_time) / NRUNS
    print("--- %s seconds ---" % (time.time() - start_time))

print("---")
print(avg)
print("---")
