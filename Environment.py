import numpy as np
import pygame
import math

SIZE = 500  # Size of Visualization (500*500)

JUMP_REWARD = 0  # Reward for normal jump
FINISH_REWARD = 100  # Reward for reaching goal
DEAD_END_PENALTY = -300  # Penalty for reaching dead end

HOLE = 1  # Formalization of board parts
FIGURE = 2
BOARD = 3

d = {1: (255, 255, 255),  # RGB values for parts
     2: (0, 0, 0),
     3: (100, 100, 100)}

JUMP_RIGHT = (1, 0)  # Movement possibilities
JUMP_LEFT = (-1, 0)
JUMP_UP = (0, -1)
JUMP_DOWN = (0, 1)

MOVES = (JUMP_RIGHT, JUMP_LEFT, JUMP_UP, JUMP_DOWN)

SCALE = 100  # Max state value to return (0 - 100)


class Board:  # Board class for solitaire

    def __init__(self):

        self.board = np.zeros((9, 9, 3), dtype=np.uint8)  # Board array for RGB values
        self.holes = np.zeros((9, 9))  # Hole positions
        self.figures = np.zeros((9, 9))  # Figure positions
        self.boundary = np.zeros((33, 2))  # Actual Board positions
        self.boundary = ((3, 1), (4, 1), (5, 1), (3, 2), (4, 2),
                         (5, 2), (1, 3), (2, 3), (3, 3), (4, 3),
                         (5, 3), (6, 3), (7, 3), (1, 4), (2, 4),
                         (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
                         (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                         (6, 5), (7, 5), (3, 6), (4, 6), (5, 6),
                         (3, 7), (4, 7), (5, 7))

        # Creating dictionary for later actions
        self.action_code = {}
        self.create_action_code()

        self.pins = 32  # Number of pins (figures) at beginning
        self.moves = []  # List for possible actions (movements)
        self.value = 0  # state value

        # Initializing game visualization
        self.game_display = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption('Solitaire')
        self.clock = pygame.time.Clock()

    # Resetting board to starting position (must be called before first game and after each game)
    def reset(self):

        # Initializing figures and holes
        for pos in self.boundary:
            self.figures[pos] = True
            self.holes[pos] = False
        self.figures[4][4] = False
        self.holes[4][4] = True

        self.update()  # Updating self.board RGB values
        self.pins = 32  # Resetting number of pins
        self.calc_moves()  # Calculating possible movements (stored in self.moves)
        self.measure()  # Calculate state value (stored in self.value)

        # Returning values
        actions = self.moves
        value = self.value
        pins = self.pins
        state = (value, pins)  # state consisting of state value and number of pins
        return state, actions

    # Updating self.board RGB values
    def update(self):
        for pos in self.boundary:
            if self.holes[pos]:
                self.board[pos] = d[HOLE]
            elif self.figures[pos]:
                self.board[pos] = d[FIGURE]

    # Displaying Board with current positioning
    def show(self):
        self.game_display.fill(d[BOARD])
        for pos in self.boundary:
            pos_list = list(pos)
            pygame.draw.circle(self.game_display, self.board[pos],
                               [(pos_list[0] + 1) * int(SIZE / 9) - int(SIZE / 18),
                                (pos_list[1] + 1) * int(SIZE / 9) - int(SIZE / 18)], int(SIZE / 30))
        pygame.display.update()

    # Visualizing game (must be called repeatedly to display)
    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.show()
        self.clock.tick(2)

    # Measuring distance between one point and the center
    @staticmethod
    def distance(pos):
        pos_list = list(pos)
        dist_x = abs(4 - pos_list[0])
        dist_y = abs(4 - pos_list[1])
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        return dist

    # Checking if one movement is possible
    def check_moves(self, pos, direction):
        pos_list = list(pos)
        direction_list = list(direction)
        figure_pos = (pos_list[0] + direction_list[0], pos_list[1] + direction_list[1])  # figure to be jumped
        new_pos = (pos_list[0] + 2 * direction_list[0], pos_list[1] + 2 * direction_list[1])    # new position
        if pos in self.boundary and new_pos in self.boundary and self.figures[pos] \
                and self.figures[figure_pos] and self.holes[new_pos]:   # positions must be in boundary,
            # current position must be figure, position to be jumped must be figure and new position must be hole
            return True
        else:
            return False

    # Calculating possible movements (stored in self.moves)
    def calc_moves(self):
        self.moves = []
        for act_key in self.action_code:
            if self.check_moves(self.action_code[act_key][0], self.action_code[act_key][1]):
                self.moves.append(act_key)

    # Calculating state value (stored in self.value)
    def measure(self):
        value = 0
        for pos in self.boundary:
            if self.figures[pos]:
                value += self.distance(pos)  # Sum of distances of figures to center
        value /= (len(self.moves) + 1) * 17.461 / SCALE  # Rescaling value to 0 - SCALE
        self.value = int(value)

    # Making a move
    def move(self, movement):
        pos1 = self.action_code[movement][0]    # current position
        pos2 = (self.action_code[movement][0][0] + self.action_code[movement][1][0],    # other figure position
                self.action_code[movement][0][1] + self.action_code[movement][1][1])
        pos3 = (self.action_code[movement][0][0] + 2 * self.action_code[movement][1][0],    # hole position
                self.action_code[movement][0][1] + 2 * self.action_code[movement][1][1])
        if movement in self.moves:  # checking if movement is legit
            self.figures[pos1] = False
            self.holes[pos1] = True
            self.figures[pos2] = False
            self.holes[pos2] = True
            self.holes[pos3] = False
            self.figures[pos3] = True
            self.update()   # Updating self.board RGB values
            self.pins -= 1  # Reducing number of pins by one

    # action command (returning state as tuple of state value and number of pins,
    # reward depending on occasion, next possible actions as list and done if no more move possible)
    def action(self, action):
        self.move(action)
        self.calc_moves()
        self.measure()
        value = self.value
        actions = self.moves
        pins = self.pins
        state = (value, pins)
        done = False
        reward = 0
        if not self.value:  # self.value is only 0 if goal is reached
            reward = FINISH_REWARD
            done = True
        elif not len(self.moves):   # dead end if no more moves possible
            reward = DEAD_END_PENALTY
            done = True
        return state, reward, actions, done

    # Creates dictionary of action codes (is being called in __init__)
    def create_action_code(self):
        code = 1
        for pos in self.boundary:
            pos_list = list(pos)
            pos_right = (pos_list[0] + 2, pos_list[1])
            pos_left = (pos_list[0] - 2, pos_list[1])
            pos_up = (pos_list[0], pos_list[1] - 2)
            pos_down = (pos_list[0], pos_list[1] + 2)
            if pos_right in self.boundary:
                self.action_code.update({code: (pos, JUMP_RIGHT)})
                code += 1
            if pos_left in self.boundary:
                self.action_code.update({code: (pos, JUMP_LEFT)})
                code += 1
            if pos_up in self.boundary:
                self.action_code.update({code: (pos, JUMP_UP)})
                code += 1
            if pos_down in self.boundary:
                self.action_code.update({code: (pos, JUMP_DOWN)})
                code += 1
