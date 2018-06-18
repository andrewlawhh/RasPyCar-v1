import obstacle, waypoint
import random

'''
This file is intended to initialize the initial information of the simulation including
agents
obstacles
waypoint

All agents, obstacles, and waypoint will have access to this file
'''

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Screen width and height should be a multiple of UNIT_SIZE

# Width and Height in pygame dimensions
DIMENSIONS = 1000

# Number of 'units' or 'blocks' on each axis
NUM_UNITS = 20

# PyGame units per block
UNIT_SIZE = DIMENSIONS // NUM_UNITS

# Initialize screen width and height
SCREEN_WIDTH = DIMENSIONS
SCREEN_HEIGHT = DIMENSIONS

# Num generations
NUM_GENERATIONS = 150

# Agent starting position
AGENT_INITIAL_X = UNIT_SIZE * (NUM_UNITS // 2)
AGENT_INITIAL_Y = UNIT_SIZE * (NUM_UNITS - 2)

# Number of obstacles
NUM_OBSTACLES = 0

# Obstacle list "constructor"
def initialize_obstacles():
    obstacles = []
    for _ in range(NUM_OBSTACLES):
        obstacles.append(obstacle.Obstacle(random.randint(SCREEN_WIDTH * 0.2, SCREEN_WIDTH * 0.8) // UNIT_SIZE * UNIT_SIZE,
                                           random.randint(SCREEN_HEIGHT * 0.2, SCREEN_HEIGHT * 0.8) // UNIT_SIZE * UNIT_SIZE
                                           )
                         )
    return obstacles

# Initialize list of obstacles
OBSTACLES = initialize_obstacles()

# Return x and y values in the first quadrant
def rand_first_quadrant():
    return UNIT_SIZE * random.randint(NUM_UNITS // 2, NUM_UNITS - 2), UNIT_SIZE * random.randint(1, NUM_UNITS // 2)

# Return x and y values in the second quadrant
def rand_second_quadrant():
    return UNIT_SIZE * random.randint(1, NUM_UNITS // 2), UNIT_SIZE * random.randint(1, NUM_UNITS // 2)

# Return x and y values in the third quadrant
def rand_third_quadrant():
    return UNIT_SIZE * random.randint(1, NUM_UNITS // 2), UNIT_SIZE * random.randint(NUM_UNITS // 2, NUM_UNITS - 2)

# Return x and y values in the fourth quadrant
def rand_fourth_quadrant():
    return UNIT_SIZE * random.randint(NUM_UNITS // 2, NUM_UNITS - 2), UNIT_SIZE * random.randint(NUM_UNITS // 2, NUM_UNITS - 2)

# Randomize the location of the waypoint
def randomize_waypoint(generation):
    global WAYPOINT

    # Get random x and y coordinate according to generation
    # if generation < NUM_GENERATIONS // 4:
    #     rand_x, rand_y = rand_first_quadrant()
    # elif NUM_GENERATIONS // 4 <= generation < NUM_GENERATIONS // 2:
    #     rand_x, rand_y = rand_second_quadrant()
    # elif NUM_GENERATIONS // 2 <= generation < 3 * NUM_GENERATIONS // 4:
    #     rand_x, rand_y = rand_third_quadrant()
    # else:
    #     rand_x, rand_y = rand_fourth_quadrant()

    rand_x, rand_y = UNIT_SIZE * random.randint(1, NUM_UNITS - 2), UNIT_SIZE * random.randint(1, NUM_UNITS - 5)

    # If waypoint would be too close to agent, re randomize
    if abs(rand_x - AGENT_INITIAL_X) < NUM_UNITS // 4 * UNIT_SIZE and \
            abs(rand_y - AGENT_INITIAL_Y) < NUM_UNITS // 4 * UNIT_SIZE:
        randomize_waypoint(generation)
    # Else, set waypoint to new coordinates
    else:
        WAYPOINT = waypoint.Waypoint(rand_x, rand_y)

# Initialize waypoint variable
WAYPOINT = randomize_waypoint(0)