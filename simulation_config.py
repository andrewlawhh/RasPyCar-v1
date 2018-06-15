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
GREEN = (0, 0, 255)

#Screen width and height should be a multiple of UNIT_SIZE
UNIT_SIZE = 50
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

AGENT_INITIAL_X = SCREEN_WIDTH * 0.25
AGENT_INITIAL_Y = SCREEN_HEIGHT * 0.75

NUM_OBSTACLES = 0

WAYPOINT_X = SCREEN_WIDTH * 0.75
WAYPOINT_Y = SCREEN_HEIGHT * 0.5

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


