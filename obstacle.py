from simulation_config import *

class Obstacle:

    def __init__(self, x, y, w = 300, h = 50):
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
