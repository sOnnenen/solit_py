import numpy as np
import random

board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

def find_valid_moves():
    presentPins = np.asarray(np.where(board == 2)).T
    list_of_valid_moves_2 = []
    for count, element in enumerate(presentPins):
        directions = find_possible_directions(element)
        if len(directions) != 0:
            list_of_valid_moves_2.append([element, directions])

    return list_of_valid_moves_2

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
    list = find_valid_moves()
    if len(list) == 0:                                                        # return 0 if there is no valid move
        return 0
    nextmove = (list[random.randint(0, len(list) - 1)])
    orientation = nextmove[1]
    move(nextmove[0], orientation[random.randint(0, len(orientation) - 1)])
    return 1                                                                  # return 1 after the board array was changed by a move

print(board, "\n")
while make_random_move():
    print(board, "\n")
'''
gamestate = True
while gamestate:
    print(board, "\n")
    list = find_valid_moves()
    if len(list) == 0:
        break
    nextmove = (list[random.randint(0,len(list)-1)])
    orientation = nextmove[1]
    move(nextmove[0],orientation[random.randint(0,len(orientation)-1)])
print(board, "\n")
'''