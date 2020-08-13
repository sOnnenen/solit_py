import numpy as np
import random
import solit_random


class State:
    def __init__(self, board):
        self.board = board
    '''
    copy current stat with copy = objekt.board.copy()
    '''
    def get_available_actions(self):
        list_of_moves = []
        present_pins = np.asarray(np.where(self.board == 2)).T
        for x in present_pins:
            if self.board[x[0]][x[1] + 1] == 2 and self.board[x[0]][x[1] + 2] == 1:
                list_of_moves.append([x, 'right'])
            if self.board[x[0]][x[1] - 1] == 2 and self.board[x[0]][x[1] - 2] == 1:
                list_of_moves.append([x, 'left'])
            if self.board[x[0] + 1][x[1]] == 2 and self.board[x[0] + 2][x[1]] == 1:
                list_of_moves.append([x, 'down'])
            if self.board[x[0] - 1][x[1]] == 2 and self.board[x[0] - 2][x[1]] == 1:
                list_of_moves.append([x, 'up'])
        return list_of_moves

    def advance(self, action):
        pin_position = action[0]
        direction = action[1]
        self.board[pin_position[0]][pin_position[1]] = 1
        if direction == "up":
            self.board[pin_position[0] - 1][pin_position[1]] = 1
            self.board[pin_position[0] - 2][pin_position[1]] = 2
        if direction == "down":
            self.board[pin_position[0] + 1][pin_position[1]] = 1
            self.board[pin_position[0] + 2][pin_position[1]] = 2
        if direction == "left":
            self.board[pin_position[0]][pin_position[1] - 1] = 1
            self.board[pin_position[0]][pin_position[1] - 2] = 2
        if direction == "right":
            self.board[pin_position[0]][pin_position[1] + 1] = 1
            self.board[pin_position[0]][pin_position[1] + 2] = 2

    def get_sample_action(self):
        valid_moves = self.get_available_actions()
        return valid_moves[random.randint(0, len(valid_moves) - 1)]

    def get_score(self):
        reward = (33 - (self.board == 2).sum())
        return reward

    def is_game_over(self):
        if not self.get_available_actions():            # is list empty?
            return True
        else:
            return False

    def print_state(self):
        print(self.board)

    def reset(self):
        self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                               [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                               [0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0],
                               [0, 0, 2, 2, 2, 1, 2, 2, 2, 0, 0],
                               [0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0],
                               [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                               [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


def play_random():
    Spiel = State(solit_random.board)
    while not Spiel.is_game_over():
        action = Spiel.get_sample_action()
        Spiel.advance(action)
    Spiel.print_state()







