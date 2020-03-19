import pygame
import solit_random
import numpy as np
import solit_options
import matplotlib.pyplot as plt
import time

start_time = time.time()  # fix starting time to calculate elapsed time
x_max, y_max = 350, 350  # horizontal, vertical
WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (122, 122, 122)

pygame.init()  # initialize
screen = pygame.display.set_mode([x_max, y_max])  # screen dimensions
clock = pygame.time.Clock()  # time
done = False

coordinates = []  # center of circles
colors = [0 for i in range(33)]  # colors of circles
for i in range(0, 7):
    coordinates.append((150,100+i*30))
    coordinates.append((180,100+i*30)) 
    coordinates.append((210,100+i*30))
    if (i < 2) or (i > 4):
        continue
    coordinates.append((90,100+i*30))
    coordinates.append((120,100+i*30))
    coordinates.append((240,100+i*30))
    coordinates.append((270,100+i*30))
    
indices = [0, 1, 2, 3, 4, 5, 9, 10, 6, 7, 8, 11,
           12, 16, 17, 13, 14, 15, 18, 19, 23, 24,
           20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32]  # order of coordinates init vs. canonical init


def transform_colors(board_array):
    counter = 0
    for j in range(0, len(board_array)):
        if board_array[j] != 0:
            colors[indices[counter]] = board_array[j]
            counter += 1


pins_left = []

while not done: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
                   
    screen.fill(GREY)  # grey background
    transform_colors(solit_random.board.flatten())

    for i in range(0, len(coordinates)):  # draw circles (will be drawn 60 times per second)
        if colors[i] == 2:
            pygame.draw.circle(screen, BLACK, coordinates[i], 11)
        elif colors[i] == 1:
            pygame.draw.circle(screen, WHITE, coordinates[i], 11)

    pygame.display.flip()  # update screen
    # pygame.time.wait(100) # delay in ms in case you want to watch the game being played live
    clock.tick(4000)  # fps # increase to decrease runtime(simple solvers), caps eventually

    if solit_random.make_random_move() == 0:  # solver (make_move()) performs a move and returns 1, else returns 0
        pins_left.append((solit_random.board == 2).sum())  # calculate remaining pins
        solit_random.board = np.array(solit_random.start_board)

    if len(pins_left) == 1000:   # set the number of games to be played
        break
pygame.quit()  # quits the game

runs = len(pins_left)
mean = np.mean(pins_left)  # now print histogram and time
n, bins, patches = plt.hist(pins_left, 31, (1, 32), density=True, histtype='bar', facecolor='g', alpha=0.75, label = 'mean = ' + str(mean))
plt.xlabel('Number of Pins')
plt.ylabel('Probability')
plt.title('Histogram of remaining pins')
plt.xlim(0, 27)
# plt.ylim(0, 0.28) #zooms in, use when you expect a top probability of < 0.25
plt.grid(True)
elapsed_time = time.time() - start_time
plt.plot([], [], ' ', label="elapsed time = " + "{0:.2f}".format(elapsed_time) + "s")
plt.plot([], [], ' ', label="# of runs = " + str(runs))
plt.legend(handlelength=0)
plt.show()
