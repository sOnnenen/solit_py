import random
import numpy as np
import pickle
import os
from collections import defaultdict


def o():
    """Returns initial value for Q_value in the Q_table"""
    # return random.random()/10000
    return 0


class QLearner:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay, name):
        self.alpha = alpha  # learning rate should be 1 since we have a deterministic environment
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.epsilon_decay = epsilon_decay  # exploration rate decay
        self.name = name
        """
        use pickle to safe q table. Otherwise just use self.q = {}
        """
        if os.path.exists(name+".pickle"):
            self.start_q_table = name+".pickle"  # None or Filename
        else:
            self.start_q_table = None

        if self.start_q_table is None:
            self.q = defaultdict(o)
        else:
            with open(self.start_q_table, "rb") as f:
                self.q = pickle.load(f)

    def update_learner(self, alpha, gamma, epsilon, epsilon_decay):
        """
        it might be good to change the parameters once the winning reward is received
        """
        self.alpha = 1
        self.gamma = 0.99  # subject of change
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

    def get_reward(self, end_state, game_over):
        """
        calculating the reward for a certain state
        """
        r = np.sum(end_state)
        # Mittelwert der Standartabweichung vom "Masse - Zentrum"
        # np.average(np.std(np.where(end_state == 1), axis=1))
        if r == 1:
            return 10000
        if game_over and (r > 1):
            return 0
        else:
            # keeping pins together might give better results on english board
            # if r < 7:
            # if np.average(np.std(np.where(end_state == 1), axis=1)) > 1.5:
            #     return 0
            # else:
            return 1

    def train_agent(self, state, actions, chosen_action, prev_state, game_over):
        """
        Calculate new q value and adjust table
        """

        reward = self.get_reward(state, game_over)
        q_before = self.get_q(prev_state, chosen_action)

        max_q_new = max([self.get_q(state, a) for a in actions], default=0)  # default case for state with no moves
        self.q[(prev_state.tobytes(), chosen_action)] = q_before + self.alpha * (
                    (reward + self.gamma * max_q_new) - q_before)
