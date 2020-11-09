import Q_Agent
import SimWorld
import numpy as np
import matplotlib.pyplot as plt
import copy
import time


def calc_epsilon_decay(epsilon, epsilon_end):
    # return (epsilon_end/epsilon)**(1/float(EPISODES))       # set to 1 for no decay
    return 1


def calc_alpha_decay(alpha, epsilon_end):
    return (alpha_end/alpha)**(1/float(EPISODES))       # set to 1 for no decay
    # return 1


EPISODES = 10000
NAME = "English normal e025 static -2.5 g %d Episodes" % EPISODES  # shows up as title of plot and name of pdf and pickle file
AVERAGE = 100


alpha = 1
gamma = [0.99, 0.65, 0.25]
epsilon_start = 0.025  # 0.99 # bei keinem decay irrelevant
epsilon_end = 0.003  # 0.005
alpha_end = 0.002 # bei keinem decay irrelevant

"""
Spielbrett aufsetzten
"""
#Brett1 = SimWorld.Diamond(6)
Brett1 = SimWorld.English()
Brett1.populate_board()
#Brett1.board_array[5][5].set_value(0)
Brett1.board_array[3][3].set_value(1)
Brett1.board_array[3][4].set_value(0)
Brett1.board_array[3][5].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()

"""
Agent aufsetzen
"""
episode_counter = 0
list_of_results = [[]]
episode_rewards = [[]]
total_rewards = [[]]
start_time = time.time()
moving_avg = [[]]
moving_avg_2 = [[]]
for i in range(3):
    AgentP = Q_Agent.QLearner(alpha, gamma[i], epsilon_start, calc_epsilon_decay(epsilon_start, epsilon_end), calc_epsilon_decay(alpha, alpha_end), NAME+str(i)) # einen decay konstant halten (1 in fkt)
    list_of_results.append([])
    episode_rewards.append([])
    total_rewards.append([])
    moving_avg.append([])
    moving_avg_2.append([])
    for element in range(EPISODES):
        episode_counter += 1
        immediate_reward = []
        while not Brett1.in_final_state():
            agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
            Brett1.take_action(agent_action)
            AgentP.train_agent(Brett1.get_board_view(), Brett1.get_actions(), agent_action, Brett1.get_previous_state(), Brett1.in_final_state())
            immediate_reward.append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))
        result = np.sum(Brett1.get_board_view())
        list_of_results[i].append(result)
        AgentP.update_epsilon()     # apply epsilon decay
        episode_rewards[i].append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))
        total_rewards[i].append(sum(immediate_reward))
        if Brett1.in_final_state():
            Brett1.set_board_array(copy.deepcopy(start_board))
    print("done")

    moving_avg[i] = np.convolve(list_of_results[i], np.ones((AVERAGE,)) / AVERAGE, mode="valid")
    moving_avg_2[i] = np.convolve(total_rewards[i], np.ones((AVERAGE,)) / AVERAGE, mode="valid")

plt.figure(0)
x = [i for i in range(len(moving_avg[1]))]
# plt.plot(x, moving_avg[0], x, moving_avg[1], x, moving_avg[2])

plt.plot(x, moving_avg[0], color='red', label='gamma = '+str(gamma[0]))
plt.plot(x, moving_avg[1], color='blue', label='gamma = '+str(gamma[1]))
plt.plot(x, moving_avg[2], color='green', label='gamma = '+str(gamma[2]))
plt.legend()
plt.title(NAME)
plt.ylabel('Remaining Pins')
plt.xlabel('Games played')
plt.grid()
# plt.show()
plt.savefig(NAME+".pdf", dpi=300)


plt.figure(1)
x2 = [i for i in range(len(moving_avg_2[1]))]
# plt.plot(x2, moving_avg_2[0], x2, moving_avg_2[1], x2, moving_avg_2[2])
plt.plot(x2, moving_avg_2[0], color='red', label='gamma = '+str(gamma[0]))
plt.plot(x2, moving_avg_2[1], color='blue', label='gamma = '+str(gamma[1]))
plt.plot(x2, moving_avg_2[2], color='green', label='gamma = '+str(gamma[2]))
plt.legend()
plt.title(NAME)
plt.ylabel('Total Reward over Episode')
plt.xlabel('Games played')
plt.grid()
plt.savefig(NAME+" Reward.pdf", dpi=300)
print("--- %s seconds ---" % (time.time() - start_time))

















