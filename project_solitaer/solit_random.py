import numpy as np
import random

start_board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

board = start_board.copy()


def find_valid_moves():
    present_pins = np.asarray(np.where(board == 2)).T
    list_of_valid_moves = []
    for element in present_pins:
        directions = find_possible_directions(element)
        if len(directions) != 0:
            for direction in directions:
                list_of_valid_moves.append([element, direction])
    return list_of_valid_moves


def move(pin_position, direction):
    board[pin_position[0]][pin_position[1]] = 1
    if direction == "up":
        board[pin_position[0]-1][pin_position[1]] = 1
        board[pin_position[0]-2][pin_position[1]] = 2
    if direction == "down":
        board[pin_position[0]+1][pin_position[1]] = 1
        board[pin_position[0]+2][pin_position[1]] = 2
    if direction == "left":
        board[pin_position[0]][pin_position[1]-1] = 1
        board[pin_position[0]][pin_position[1]-2] = 2
    if direction == "right":
        board[pin_position[0]][pin_position[1]+1] = 1
        board[pin_position[0]][pin_position[1]+2] = 2


def find_possible_directions(x):
    list_of_directions = []
    if board[x[0]][x[1]+1] == 2 and board[x[0]][x[1]+2] == 1:
        list_of_directions.append('right')
    if board[x[0]][x[1]-1] == 2 and board[x[0]][x[1]-2] == 1:
        list_of_directions.append('left')
    if board[x[0]+1][x[1]] == 2 and board[x[0]+2][x[1]] == 1:
        list_of_directions.append('down')
    if board[x[0]-1][x[1]] == 2 and board[x[0]-2][x[1]] == 1:
        list_of_directions.append('up')
    return list_of_directions


def make_random_move():
    valid_m = find_valid_moves()
    if len(valid_m) == 0:  # return 0 if there is no valid move
        return 0
    rand_move = valid_m[random.randint(0, len(valid_m) - 1)]
    move(rand_move[0], rand_move[1])
    return 1  # return 1 after the board array was changed by a move
