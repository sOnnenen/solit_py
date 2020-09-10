import random
import SimWorld
import numpy as np
import copy
import matplotlib.pyplot as plt
import math
import pickle
import os
from collections import defaultdict

EPISODES = 25000
SHOW_EVERY = 5000
reward_dict = {1: 500, 2: 4, 3: 0.06, 4: 0.002, 5: 0.0001, 6: 0.000015}  # rewards for pins left


def calc_epsilon_decay(epsilon, epsilon_end):
    return (epsilon_end/epsilon)**(1/float(EPISODES))


def o():
    return 0  # needed to make default_dict work


class QLearner:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay):
        self.alpha = alpha  # learning rate should be 1 since we have a deterministic environment
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.epsilon_decay = epsilon_decay  # exploration rate decay
        """
        use pickle to safe q table. Otherwise just use self.q = {}
        """
        if os.path.exists("English_10000.pickle"):
            self.start_q_table = "English_10000.pickle"  # None or Filename
        else:
            self.start_q_table = None

        if self.start_q_table is None:
            self.q = defaultdict(o)
        else:
            with open(self.start_q_table, "rb") as f:
                self.q = pickle.load(f)

    def update_learner(self):
        """
        it might be good to change the parameters once the winning reward is received
        """
        self.alpha = 1
        self.gamma = 0.9  # subject of change
        self.epsilon = 0.05  # subject of change

    def update_epsilon(self):
        """
        applying decay to epsilon (epsilon = chance to make a random move instead of max q move)
        """
        self.epsilon *= self.epsilon_decay

    def get_q(self, state, action):
        """
        return Q value for state - action pair. 0 initially by default dict
        state is transformed into bytes to be able to act as key
        """
        return self.q[(state.tobytes(), action)]

    def get_next_action(self, state, actions):
        """
        get the action based on q table or random in case of exploration
        """
        current_state = state
        if random.random() < self.epsilon:  # exploring
            chosen_action = random.choice(actions)
            return chosen_action
        q_values = [self.get_q(current_state, a) for a in actions]
        max_q = max(q_values)

        if q_values.count(max_q) > 1:
            best_options = [i for i in range(len(actions)) if q_values[i] == max_q]  # multiple best options
            i = random.choice(best_options)
        else:
            i = q_values.index(max_q)
        return actions[i]

    def get_reward(self, end_state):
        """
        calculating the reward for a certain state
        """
        r = np.sum(end_state)
        if r < 7:
            return reward_dict[r]
        else:   # threshold can be added to use update learner function
            return 0

    def train_agent(self, state, actions, chosen_action, prev_state, game_over):
        """
        Calculate new q value and adjust table
        """
        reward = 0
        if game_over:
            reward = self.get_reward(state)
        #
        q_before = self.get_q(prev_state, chosen_action)
        max_q_new = max([self.get_q(state, a) for a in actions], default=0)  # default case for state with no moves
        self.q[(prev_state.tobytes(), chosen_action)] = q_before + self.alpha * (
                    (reward + self.gamma * max_q_new) - q_before)

"""
    Brett1 = SimWorld.Triangular(5)
    Brett1.populate_board()
    Brett1.board_array[0][0].set_value(0)
    Brett1.set_neighbor_pairs()
    start_board = Brett1.get_board_copy()
    # Setup Board is now done
    
    AgentP = QLearner(1, 0.99, 0.96, calc_epsilon_decay(0.96, 0.01))
    episode_counter = 0
    list_of_results = []
    episode_rewards = []
    total_rewards = np.zeros(EPISODES)  # graph reward achieved by qlearner (where does progress come from)
    
    for element in range(EPISODES):
        episode_counter += 1
        while not Brett1.in_final_state():
            agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
            Brett1.take_action(agent_action)
            AgentP.train_agent(Brett1.get_board_view(), Brett1.get_actions(), agent_action, Brett1.get_previous_state(), Brett1.in_final_state())
        result = np.sum(Brett1.get_board_view())
        list_of_results.append(result)
        if episode_counter % SHOW_EVERY == 0:
            print("Result: ", result)
            print(Brett1.get_board_view())
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
    
    
    # uncomment if using moving average
    # moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
    
    
    plt.plot(list_of_results)
    plt.show()
    
    
    # plt.plot([i for i in range(len(moving_avg))], moving_avg)
    # plt.ylabel(f"reward {SHOW_EVERY}ma")
    # plt.xlabel("episode #")
    # plt.show()
    
    with open(f"Triangle_5.pickle", "wb") as f:
        pickle.dump(AgentP.q, f, protocol=1)
"""
