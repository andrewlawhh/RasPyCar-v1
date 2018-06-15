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
UNIT_SIZE = 50
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

# Num generations
NUM_GENERATIONS = 200

# Agent position
AGENT_INITIAL_X = SCREEN_WIDTH * 0.20
AGENT_INITIAL_Y = SCREEN_HEIGHT * 0.60

# Waypoint position
WAYPOINT_X = SCREEN_WIDTH * 0.60
WAYPOINT_Y = SCREEN_HEIGHT * 0.40

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

OBSTACLES = initialize_obstacles()
WAYPOINT = waypoint.Waypoint()


