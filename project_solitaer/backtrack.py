import solit_random
moves_to_victory = []


def play_move_to_victory():
    """
    Plays moves created by solve_solitaer() backtracking algorithm
    """
    if len(moves_to_victory) == 0:
        return 0
    move = moves_to_victory[0]
    solit_random.move(move[0], move[1])
    moves_to_victory.pop(0)
    return 1


def solve_solitaer():
    """
    uses Backtracking to get a solution for the solitaer puzzle and saves the necessary moves in moves_to_victory
    """
    #  Analog zu N-Damen Problem https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/
    #  https://www.youtube.com/watch?v=0DeznFqrgAI
    if(solit_random.board == 2).sum() == 1 and solit_random.board[5][5] == 2:
        return True
    else:
        posb_moves = solit_random.find_valid_moves()
        for i in range(31):
            if len(posb_moves) == 0:
                return False
            previous_board = solit_random.board.copy()
            current_move = posb_moves[0]
            moves_to_victory.append(current_move)
            solit_random.move(current_move[0], current_move[1])
            if solve_solitaer() is True:
                return True
            posb_moves.pop(0)  # pops first element of list, for higher performance look at collections.deque
            moves_to_victory.pop()  # pops last element
            solit_random.board = previous_board.copy()
