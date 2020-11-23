import numpy as np
import pygame
import math

SIZE = 500  # Size of Visualization (500*500)

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
DO_NOTHING = ((0, 0), (0, 0))

MOVES = (JUMP_RIGHT, JUMP_LEFT, JUMP_UP, JUMP_DOWN)


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

        self.value_board = np.zeros((9, 9))
        self.center = np.zeros((9, 9))
        i = 0
        for pos in self.boundary:
            if i in (0, 2, 6, 12, 20, 26, 30, 32):
                self.value_board[pos] = 11250
                self.center[pos] = 6
            elif i in (1, 13, 19, 31):
                self.value_board[pos] = 2250
                self.center[pos] = 5
            elif i in (3, 5, 7, 11, 21, 25, 27, 29):
                self.value_board[pos] = 250
                self.center[pos] = 4
            elif i in (4, 14, 18, 28):
                self.value_board[pos] = 50
                self.center[pos] = 3
            elif i in (8, 10, 22, 24):
                self.value_board[pos] = 10
                self.center[pos] = 2
            elif i in (9, 15, 17, 23):
                self.value_board[pos] = 2
                self.center[pos] = 1
            else:
                self.value_board[pos] = 1
            i += 1

        # Creating dictionary for later actions
        self.action_code = {}
        self.create_action_code()

        self.pins = 32  # Number of pins (figures) at beginning
        self.moves = []  # List for possible actions (movements)

        self.jump_reward = 1
        self.finish_reward = 10000
        self.dead_end_penalty = -1000

        # Initializing game visualization
        self.game_display = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption('Solitaire')
        self.clock = pygame.time.Clock()

    def set_params(self, jump_reward, finish_reward, dead_end_penalty):
        self.jump_reward = jump_reward
        self.finish_reward = finish_reward
        self.dead_end_penalty = dead_end_penalty

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

        # Returning values
        actions = self.moves
        value, center = self.get_state_value()
        pins = self.pins
        state = (value, center)  # state consisting of state value and number of pins
        return state, pins, actions

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
        self.clock.tick(1000)

    def save_game(self, filename):
        pygame.image.save(self.game_display, filename)

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
        if action is not DO_NOTHING:
            self.move(action)
        self.calc_moves()
        value, center = self.get_state_value()
        actions = self.moves
        pins = self.pins
        state = (value, center)
        done = False
        if not len(self.moves):
            done = True
        reward = self.get_reward()
        return state, pins, reward, actions, done

    def get_state_value(self):
        value = 0
        center = 0
        dist = 1000
        for pos in self.boundary:
            if self.figures[pos]:
                value += self.value_board[pos]
            if self.sum_dist(pos) < dist:
                center = self.center[pos]
                dist = self.sum_dist(pos)
            elif self.sum_dist(pos) is dist:
                if self.center[pos] < center:
                    center = self.center[pos]
                    dist = self.sum_dist(pos)
        value = int(value)
        center = int(center)
        return value, center

    @staticmethod
    def dist(pos1, pos2):
        pos1_list = list(pos1)
        pos2_list = list(pos2)
        dist_x = abs(pos2_list[0] - pos1_list[0])
        dist_y = abs(pos2_list[1] - pos1_list[1])
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        return dist

    def sum_dist(self, pos):
        sum_dist = 0
        for fig in self.boundary:
            if self.figures[fig]:
                sum_dist += self.dist(pos, fig)
        return sum_dist

    def get_reward(self):
        value, center = self.get_state_value()
        reward = self.jump_reward * 1
        if value == 1:  # self.value is only 0 if goal is reached
            reward = self.finish_reward
        elif not len(self.moves):  # dead end if no more moves possible
            reward = self.dead_end_penalty * value / 1000
        return reward

    # Creates dictionary of action codes (is being called in __init__)
    def create_action_code(self):
        code = 0
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

    # Returns number of  theoretically possible actions
    def action_space(self):
        space = len(self.action_code)
        return space

    @staticmethod
    # Returns number of possible states
    def observation_space():
        space = [101250, 7]
        return space

    # Loading board randomly with number of pins (2 - 32)
    def load_board(self, pins):
        self.pins = pins
        for pos in self.boundary:
            self.figures[pos] = False
            self.holes[pos] = True
        self.figures[4][4] = True
        self.holes[4][4] = False
        if pins > 1:
            pins -= 1
            while pins:
                possible_pos = []
                for pos in self.boundary:
                    if self.figures[pos]:
                        pos_list = list(pos)
                        for move in MOVES:
                            move_list = list(move)
                            new_fig = (pos_list[0] + move_list[0], pos_list[1] + move_list[1])
                            new_pos = (pos_list[0] + 2 * move_list[0], pos_list[1] + 2 * move_list[1])
                            if new_pos in self.boundary and self.holes[new_pos] and self.holes[new_fig]:
                                possible_pos.append([pos, new_fig, new_pos])
                if len(possible_pos):
                    new = possible_pos[np.random.randint(0, len(possible_pos))]
                    self.figures[new[0]] = False
                    self.holes[new[0]] = True
                    self.figures[new[1]] = True
                    self.holes[new[1]] = False
                    self.figures[new[2]] = True
                    self.holes[new[2]] = False
                    pins -= 1
                else:
                    break
        self.update()
        state, pins, reward, actions, done = self.action(DO_NOTHING)
        return state, pins, actions
