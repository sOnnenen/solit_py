import pygame
import Q_Agent
import SimWorld
import numpy as np
import matplotlib.pyplot as plt
import copy
import pickle
import time


WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (122, 122, 122)        # Colors for Peg, no Peg, Background


class Screen:
    def __init__(self, game_board):
        self.game_board = game_board
        self.board = game_board.get_board_view()  # get array with pins as 0 and 1
        self.WHITE, self.BLACK, self.GREY = (255, 255, 255), (0, 0, 0), (122, 122, 122)
        self.size = game_board.get_board_view().shape[0]
        self.x_max, self.y_max = game_board.get_board_view().shape[0] * 100, game_board.get_board_view().shape[0] * 100  # horizontal, vertical
        self.screen = pygame.display.set_mode([self.x_max, self.y_max])  # screen dimensions
        self.center = self.x_max//2
        self.offset = self.center - (self.size-1)*25

    def open_screen(self):
        """
        calculates the screen for the current board
        """
        self.board = self.game_board.get_board_view()
        self.screen.fill(GREY)
        if self.game_board.board_shape == "Diamond":
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[j][i] == 1:
                        pygame.draw.circle(self.screen, self.BLACK, (self.offset+50*i, self.offset+j*50), 15)
                    if self.board[j][i] == 0:
                        pygame.draw.circle(self.screen, self.WHITE, (self.offset + 50 * i, self.offset + j * 50), 15)

            self.screen.blit(pygame.transform.rotate(self.screen, 45), (-25*self.size-1, -25*self.size-1))
        if self.game_board.board_shape == "Triangular":
            for i in range(self.size):
                for j in range(self.size):
                    if self.game_board.get_board_array()[j][i] != 0:
                        if j < self.size -1:
                            dist = self.center - self.offset
                        else:
                            dist = 0
                        shift = (dist * (self.size-j-1))//(self.size-1)
                        if self.board[j][i] == 1:
                            pygame.draw.circle(self.screen, self.BLACK, (self.offset+50*i+shift, self.offset+j*50), 15)
                        if self.board[j][i] == 0:
                            pygame.draw.circle(self.screen, self.WHITE, (self.offset + 50 * i+shift, self.offset + j * 50), 15)

    def update_screen(self, wait_time, fps):
        """
        updates display, introduces delay and fps
        """
        pygame.display.flip()
        pygame.time.wait(wait_time)  # delay in ms in case you want to watch the game being played live
        clock.tick(fps)  # fps # increase to decrease runtime(simple solvers), caps eventually

#  Setup the Board
Brett1 = SimWorld.Triangular(5)
Brett1.populate_board()
Brett1.board_array[0][0].set_value(0)
Brett1.set_neighbor_pairs()
print(Brett1.get_board_view())
start_board = Brett1.get_board_copy()
# Setup Q_Agent
AgentP = Q_Agent.QLearner(1, 0.9, 0.96, 0.997)
episode_counter = 0
list_of_results = []
episode_rewards = []
total_rewards = np.zeros(Q_Agent.EPISODES)
display_flag = 0
# Setup Display
Display = Screen(Brett1)
start_time = time.time()  # fix starting time to calculate elapsed time
pygame.init()
clock = pygame.time.Clock()  # time
Display.open_screen()
Display.update_screen(500, 600)
# Play Episodes, show the game from time to time
for element in range(Q_Agent.EPISODES):
    episode_counter += 1
    while not Brett1.in_final_state():
        if display_flag == 1:
            Display.open_screen()
            Display.update_screen(500, 600)
        agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
        Brett1.take_action(agent_action)
        AgentP.train_agent(Brett1.get_board_view(), Brett1.get_actions(), agent_action, Brett1.get_previous_state(), Brett1.in_final_state())
        if display_flag == 1:
            Display.open_screen()
            Display.update_screen(500, 600)
    result = np.sum(Brett1.get_board_view())
    list_of_results.append(result)
    if episode_counter % Q_Agent.SHOW_EVERY == 0:
        display_flag = 1
        print("Result: ", result)
        print(Brett1.get_board_view())
    else:
        display_flag = 0
    AgentP.update_epsilon()     # apply epsilon decay
    episode_rewards.append(AgentP.get_reward(Brett1.get_board_view()))
    total_rewards[element] = AgentP.get_reward(Brett1.get_board_view())
    if Brett1.in_final_state():
        Brett1.set_board_array(copy.deepcopy(start_board))


AgentP.epsilon = 0
print("best way")
while not Brett1.in_final_state():
    agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
    Brett1.take_action(agent_action)
print(Brett1.get_board_view())

"""
# uncomment if using moving average
moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
"""

plt.plot(list_of_results)
plt.show()
"""

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()
"""
with open(f"q_table_1.pickle", "wb") as f:
    pickle.dump(AgentP.q, f, protocol=pickle.HIGHEST_PROTOCOL)



