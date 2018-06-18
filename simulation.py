import pygame
from agent import Unit
from simulation_config import *
import time

class Simulation:
    simulation_number = 0

    def __init__(self, genomes, config):
        print('simulation number', Simulation.simulation_number)

        global SCREEN, FPSCLOCK

        # Initialize PyGame
        pygame.init()

        # Set FPS manager
        FPSCLOCK = pygame.time.Clock()

        # Set SCREEN surface variable
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set screen caption
        pygame.display.set_caption('RPyCar Simulation PoC')

        # Randomize location of the waypoint
        randomize_waypoint(Simulation.simulation_number)

        # Initialize agents
        self.agents = [Unit(genome, config) for genome in genomes]

        # Initialize obstacles, from agent instance variable (all of them refer to the same list of obstacles)
        self.obstacles = self.agents[0].obstacles

        # Initialize waypoint
        self.waypoint = self.agents[0].waypoint

        # Initialize finish info array, to be passed to fitness function in training script
        self.finish_info = []

    # Main loop
    # Runs simulation for one generation
    def run_simulation(self, slow_mode = False):

        # Loop until finished or exit event
        while True:
            # Handles quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            # Sleeps before rendering if slow_mode is on
            if slow_mode:
                time.sleep(.05)
            # Terminate loop if simulation finish conditions are met
            if self.finished():
                #print('generation finished')
                Simulation.simulation_number += 1
                return
            # Update the locations of the agents and render the screen
            else:
                #print(20 * '*')
                self.update_agents()
                self.render_next_frame()

    '''
    Termination methods
    '''

    # Returns a boolean
    # True if all agents are either dead or have reached the waypoint
    # False if at least one agent is still alive and has not reached the waypoint
    def finished(self):
        for agent in self.agents:
            if not agent.dead and not agent.reached_waypoint:
                return False
        self.set_finish_info()
        return True

    # Args : None | Returns : None
    # Collects finish info from each agent to be returned to fitness function in training script
    def set_finish_info(self):
        for agent in self.agents:
            self.finish_info.append(agent.finish_info)

    '''
    Methods that show the next actions to the screen
    '''

    # Args : None, Returns: None
    # Updates each agent
    def update_agents(self):
        # Update agent positions
        for agent in self.agents:
            agent.update()

    # Displays the next frame to the screen
    def render_next_frame(self):
        #print("rendering next frame")

        # Draw background (fill with white)
        SCREEN.fill(WHITE)

        # Draw grid
        self.draw_grid()

        # Draw Agents
        self.draw_agents()

        # Draw Obstacles
        self.draw_obstacles()

        # Draw Waypoint
        self.draw_waypoint()

        # Draw Stats
        self.draw_stats()

        pygame.display.update()
        FPSCLOCK.tick(60)

    '''
    Drawing methods
    '''

    # Draw grid
    def draw_grid(self):
        #print('drawing grid')
        # Draw horizontal lines
        y = 0
        while y < SCREEN_HEIGHT:
            start_pos = (0, y)
            end_pos = (SCREEN_WIDTH, y)
            pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
            y += UNIT_SIZE

        # Draw vertical lines
        x = 0
        while x < SCREEN_WIDTH:
            start_pos = (x, 0)
            end_pos = (x, SCREEN_HEIGHT)
            pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
            x += UNIT_SIZE

    # Draw agents
    def draw_agents(self):
        #print('drawing agents')
        for agent in self.agents:
            if agent.reached_waypoint:
                color = GREEN
            else:
                color = BLACK
            agent_rect = pygame.Rect(agent.x_pos, agent.y_pos, UNIT_SIZE, UNIT_SIZE)
            pygame.draw.rect(SCREEN, color, agent_rect)

    # Draw obstacles
    def draw_obstacles(self):
        #print('drawing obstacles')
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle.x_pos, obstacle.y_pos, obstacle.width, obstacle.height)
            pygame.draw.rect(SCREEN, RED, obstacle_rect)

    # Draw waypoint
    def draw_waypoint(self):
        #print('drawing waypoint')
        #
        # waypoint_rect = pygame.Rect(self.waypoint.x_pos, self.waypoint.y_pos, UNIT_SIZE, UNIT_SIZE)
        # pygame.draw.rect(SCREEN, GREEN, waypoint_rect)
        waypoint_rect = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
        waypoint_rect.set_alpha(128)
        waypoint_rect.fill(BLUE)
        SCREEN.blit(waypoint_rect, (self.waypoint.x_pos, self.waypoint.y_pos))

    # Draw stats
    def draw_stats(self):
        pass
