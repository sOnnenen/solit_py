from tensorflow.keras import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import game
import solit_random
import numpy as np
import matplotlib.pyplot as plt


eta = 0.1  # learning rate
policy = Sequential()
policy.add(Dense(33, input_shape =(33,),activation='relu'))
policy.add(Dense(33, kernel_initializer=initializers.RandomNormal(stddev=0.01),
                 bias_initializer=initializers.Zeros(), activation='relu'))
policy.add(Dense(33, kernel_initializer=initializers.RandomNormal(stddev=0.01),
                 bias_initializer=initializers.Zeros(), activation='relu'))
policy.add(Dense(1, kernel_initializer=initializers.RandomNormal(stddev=0.01),
                 bias_initializer=initializers.Zeros(), activation='relu'))

policy.compile(loss='mean_squared_error', optimizer=optimizers.SGD(lr=eta), metrics=['accuracy'])


def calculate_value(board):
    """
    calculates value of board state
    returns prediction of our net(policy)
    """
    board = board[board != 0]
    return policy.predict(board.reshape(1, 33))


def play_x_random_games(x):
    """
    returns trajectories and scores for x random games
    """
    states = []
    list_of_states_and_scores = []
    Game = game.State(solit_random.board)
    for i in range(x):
        while not Game.is_game_over():
            action = Game.get_sample_action()
            Game.advance(action)
            states.append(Game.board.copy())

        score = Game.get_score()
        Game.reset()
        list_of_states_and_scores.append([states.copy(), score])
        states = []
    return list_of_states_and_scores


def count_unique_terminal_states(batch):
    last_elements = []
    uniques = []
    for i in range(len(batch)):
        run = y[i]
        trajectory = run[0]
        last_elements.append(trajectory[-1])
    for arr in last_elements:
        if not any(np.array_equal(arr, unique_arr) for unique_arr in uniques):
            uniques.append(arr)

    return len(last_elements)-len(uniques)


def train_net(batch):
    # batch is [[board],reward]
    # obs should be [board.reshape(1, 33)]
    # rew should be [reward]
    obs = []
    rew = []
    for i in range(len(batch)):
        elements = batch[i]
        boards = elements[0]
        value = elements[1]
        for j in range(len(boards)):
            element = boards[j]
            element = element[element != 0]
            obs.append(element)
            rew.append(np.exp(value/(2*(33-j))))
    policy.train_on_batch(np.array(obs), np.array(rew))


def nn_play(Game):
    if (Game.board == 2).sum() > (32 - n):
        chosen_action = Game.get_sample_action()
    else:
        if np.random.rand(1) < e:
            chosen_action = Game.get_sample_action()

        else:
            actions = Game.get_available_actions()
            list_of_values = []
            if len(actions) == 0:
                return # game over
            for action in range(len(actions)):
                next_action = actions[action]
                Game_new = game.State(Game.board.copy())
                Game_new.advance(next_action)
                list_of_values.append(calculate_value(Game_new.board))
            m = list_of_values.index(max(list_of_values))
            chosen_action = actions[m]

    return chosen_action


def play_x_learning_games(games_to_be_played):
    """
    returns trajectories and scores for x random games
    """

    list_of_states_and_scores = []
    Game = game.State(solit_random.start_board.copy())
    for number_of_games in range(games_to_be_played):
        states = []
        current_state = 0
        while not Game.is_game_over():
            current_state = current_state + 1
            Game.advance(nn_play(Game))
            if current_state > training_threshold:
                states.append(Game.board.copy())
        score = Game.get_score()
        list_of_states_and_scores.append([states.copy(), score])
        Game.reset()

    return list_of_states_and_scores


def calculate_left_pins(batch_of_games):
    remaining_pins = []
    for batch_of_states in range(len(batch_of_games)):
        episode = batch_of_games[batch_of_states]
        element = episode[0]
        remaining_pins.append((element[-1] == 2).sum())  # calculate pins left
    return remaining_pins


def make_plot(mean_value, pins, runs):
    x, bins, patches = plt.hist(pins, 31, (1, 32), density=True, histtype='bar', facecolor='g', alpha=0.75, label = 'mean = ' + str(mean_value))
    plt.xlabel('Number of Pins')
    plt.ylabel('Probability')
    plt.title('Histogram of remaining pins')
    plt.xlim(0, 27)
    # plt.ylim(0, 0.28) #zooms in, use when you expect a top probability of < 0.25
    plt.grid(True)
    plt.plot([], [], ' ', label="# of runs = " + str(runs))
    plt.legend(handlelength=0)
    plt.show()  # The plot does not appear.
#    plt.draw()             # The plot does not appear.
#    plt.pause(0.1)          # The plot properly appears.


def print_stats(batch):
    runs = len(batch)
    pins_left = calculate_left_pins(batch)
    mean = np.mean(pins_left)
    print("After ", runs, " runs, there are on average ", mean, "pins left.")


e = 0                         # Chance of AI making a random move instead of calculated one
training_threshold = 5        # Threshold for moves that need to be played on a board to include board in training data
n = 5                         # number of random moves to be played at the start of each game

for count in range(5):
    y_train = play_x_learning_games(3)
    print_stats(y_train)
    train_net(y_train)
