import pygame
import Q_Agent
import SimWorld
import numpy as np
import matplotlib.pyplot as plt
import copy
import pickle
import time

EPISODES = 1000
SHOW_EVERY = 999  # don't show to not slow down training
WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (122, 122, 122)        # Colors for Peg, no Peg, Background
# NAME = "Triangular 6 %d Episodes" % EPISODES  # shows up as title of plot and name of pdf and pickle file
NAME = "Pinguin_test"
show_games = 1
time_between_displayed_moves = 50  # number is in ms
AVERAGE = 20


alpha = 1
gamma = 0.99
epsilon_start = 0.99  # 0.99
epsilon_end = 0.003  # 0.005
alpha_end = 0.003

def calc_epsilon_decay(epsilon, epsilon_end):
    return (epsilon_end/epsilon)**(1/float(EPISODES))


def calc_alpha_decay(alpha, alpha_end):
    return 1


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

        if self.game_board.board_shape == "English":
            for i in range(self.size):
                for j in range(self.size):
                    if self.game_board.board_array[j][i] == 0:
                        pygame.draw.circle(self.screen, self.GREY, (self.offset + 50 * i, self.offset + j * 50), 15)
                    elif self.game_board.board_array[j][i].get_value() == 1:
                        pygame.draw.circle(self.screen, self.BLACK, (self.offset+50*i, self.offset+j*50), 15)
                    elif self.game_board.board_array[j][i].get_value() == 0:
                        pygame.draw.circle(self.screen, self.WHITE, (self.offset + 50 * i, self.offset + j * 50), 15)


    def update_screen(self, wait_time, fps):
        """
        updates display, introduces delay and fps
        """
        pygame.display.flip()
        pygame.time.wait(wait_time)  # delay in ms in case you want to watch the game being played live
        clock.tick(fps)  # fps # increase to decrease runtime(simple solvers), caps eventually

#  Setup the Board
Brett1 = SimWorld.Penguin()
# Brett1 = SimWorld.Diamond(6)
Brett1.populate_board()
# make first move as it does not really matter
# Brett1.board_array[3][3].set_value(1)
# Brett1.board_array[3][4].set_value(0)
# Brett1.board_array[3][5].set_value(0)
Brett1.board_array[2][1].set_value(0)

Brett1.set_neighbor_pairs()
print(Brett1.get_board_view())
start_board = Brett1.get_board_copy()
# Setup Q_Agent
AgentP = Q_Agent.QLearner(alpha, gamma, epsilon_start, calc_epsilon_decay(epsilon_start, epsilon_end), calc_alpha_decay(alpha, alpha_end), NAME)
episode_counter = 0
list_of_results = []
episode_rewards = []
total_rewards = np.zeros(EPISODES)
start_time = time.time()  # fix starting time to calculate elapsed time

if show_games == 1:
    Display = Screen(Brett1)
    pygame.init()
    clock = pygame.time.Clock()  # time
    Display.open_screen()
    Display.update_screen(time_between_displayed_moves, 600)
display_flag = 0
# Play Episodes, show the game from time to time
for element in range(EPISODES):
    episode_counter += 1
    immediate_reward = []
    while not Brett1.in_final_state():
        if display_flag == 1:
            Display.open_screen()
            Display.update_screen(time_between_displayed_moves, 600)
        agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
        Brett1.take_action(agent_action)
        AgentP.train_agent(Brett1.get_board_view(), Brett1.get_actions(), agent_action, Brett1.get_previous_state(), Brett1.in_final_state())
        immediate_reward.append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))
        if display_flag == 1:
            Display.open_screen()
            Display.update_screen(time_between_displayed_moves, 600)
    result = np.sum(Brett1.get_board_view())
    list_of_results.append(result)
    if episode_counter % SHOW_EVERY == 0 and show_games:
        display_flag = 1
        print("Result: ", result)
        print(Brett1.get_board_view())
    else:
        display_flag = 0
    AgentP.update_epsilon()     # apply epsilon decay
    AgentP.update_alpha()
    episode_rewards.append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))    # maybe move reward function to teacher
    total_rewards[element] = sum(immediate_reward)
    if Brett1.in_final_state():
        Brett1.set_board_array(copy.deepcopy(start_board))


AgentP.epsilon = 0
print("best way")
while not Brett1.in_final_state():
    agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
    Brett1.take_action(agent_action)
print(Brett1.get_board_view())
print("Max given reward was", max(episode_rewards))

moving_avg = np.convolve(list_of_results, np.ones((AVERAGE,)) / AVERAGE, mode="valid")
plt.figure(0)
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.title(NAME)
plt.ylabel('Remaining Pins')
plt.xlabel('Games played')
plt.grid()
# plt.show()
plt.savefig(NAME+".pdf", dpi=300)


moving_avg_2 = np.convolve(total_rewards, np.ones((AVERAGE,)) / AVERAGE, mode="valid")
plt.figure(1)
plt.plot([i for i in range(len(moving_avg_2))], moving_avg_2)
plt.title(NAME)
plt.ylabel('Total Reward over Episode')
plt.xlabel('Games played')
plt.grid()
plt.savefig(NAME+" Reward.pdf", dpi=300)


with open(NAME+f".pickle", "wb") as f:
    pickle.dump(AgentP.q, f, protocol=pickle.HIGHEST_PROTOCOL)

print("--- %s seconds ---" % (time.time() - start_time))
