import random
import numpy as np
import pickle
import os
from collections import defaultdict

ACTIVE_FUNCTION = 'normalized_reward'

goal_reached = False

def normalized_reward(dead_end, end_state):
    pins_left = np.sum(end_state)
    if pins_left == 1:
        return 10000
    if dead_end is True:
        return -2
    else:
        return 1


def strict_reward(dead_end, end_state):
    pins_left = np.sum(end_state)
    if pins_left == 1:
        global goal_reached
        goal_reached = True
        return 10
    elif dead_end is True:
        return -0.9
    else:
        return 1
# test only negativ reward (when game is over)
# test adjusting learning rate when goal is reached ()


def tactical_reward(dead_end, end_state):
    pins_left = np.sum(end_state)
    if pins_left == 1:
        return 10000
    if dead_end is True:
        return -11
    if (25 > pins_left) and (10 < pins_left):
        if np.average(np.std(np.where(end_state == 1), axis=1)) > 1.5:
            return -1
        else:
            return 0
    else:
        return 0


reward_function_dict = {
    'normalized_reward': normalized_reward,
    'strict_reward': strict_reward,
    'tactical_reward': tactical_reward
}


def get_reward(end_state, game_over):
    """
    calculating the reward for a certain state
    """
    return reward_function_dict[ACTIVE_FUNCTION](game_over, end_state)


def o():
    """Returns initial value for Q_value in the Q_table"""
    return 0


class QLearner:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay, alpha_decay, name):
        self.alpha = alpha      # learning rate should be 1 since we have a deterministic environment
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate
        self.epsilon_decay = epsilon_decay  # exploration rate decay
        self.alpha_decay = alpha_decay
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

    def update_learner(self):
        """
        it might be good to change the parameters once the winning reward is received
        """
        # self.alpha = (1-self.alpha)/100 + self.alpha
        # self.alpha = self.alpha - self.alpha / 50
        # self.epsilon = self.epsilon - self.epsilon/50

    def update_epsilon(self):
        """
        applying decay to epsilon (epsilon = chance to make a random move instead of max q move)
        """
        self.epsilon *= self.epsilon_decay

    def update_alpha(self):
        """
        applying decay to epsilon (epsilon = chance to make a random move instead of max q move)
        """
        self.alpha *= self.alpha_decay

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

    def train_agent(self, state, actions, chosen_action, prev_state, game_over):
        """
        Calculate new q value and adjust table
        """
        reward = get_reward(state, game_over)
        q_before = self.get_q(prev_state, chosen_action)
        max_q_new = max([self.get_q(state, a) for a in actions], default=0)  # default case for state with no moves
        self.q[(prev_state.tobytes(), chosen_action)] = q_before + self.alpha * (
                (reward + self.gamma * max_q_new) - q_before)

