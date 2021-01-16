import SimWorld
import matplotlib.pyplot as plt
import time
import numpy as np
import copy

EPISODES = 100000


"""
Brett1 = SimWorld.English()
Brett1.populate_board()
Brett1.board_array[3][3].set_value(1)
Brett1.board_array[3][4].set_value(0)
Brett1.board_array[3][5].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()
"""

Brett1 = SimWorld.Triangular(8)
Brett1.populate_board()
Brett1.board_array[0][0].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()


"""
Brett1 = SimWorld.Diamond(6)
Brett1.populate_board()
Brett1.board_array[0][0].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()
"""


def play_random_games():
    start_time = time.time()
    scores = []
    for i in range(EPISODES):
        running = True
        while running:
            Brett1.take_action(Brett1.get_sample_action())

            if Brett1.in_final_state():
                scores.append((Brett1.get_board_view() == 1).sum())
                running = False
        Brett1.set_board_array(copy.deepcopy(start_board))

    mean = np.mean(scores)  # now print histogram and time
    n, bins, patches = plt.hist(scores, 31, (1, 32), density=True, histtype='bar', facecolor='g', alpha=0.75, label='mean = ' + str(mean))
    plt.xlabel('Number of Pins')
    plt.ylabel('Probability')
    plt.title('Histogram of remaining pins')
    plt.xlim(0, 27)
    # plt.ylim(0, 0.28) #zooms in, use when you expect a top probability of < 0.25
    plt.grid(True)
    elapsed_time = time.time() - start_time
    plt.plot([], [], ' ', label="elapsed time = " + "{0:.2f}".format(elapsed_time) + "s")
    plt.plot([], [], ' ', label="# of runs = " + str(EPISODES))
    plt.legend(handlelength=0)
    plt.show()


play_random_games()
