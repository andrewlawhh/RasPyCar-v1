import pygame

'''
Tester script
'''

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 0, 255)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('RPyCar Simulation PoC')

class TestAgent():
    def __init__(self, x, y):
        self.x = x
        self.y = y

agents = []
agents.append(TestAgent(200, 450))

def run_simulation():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        render_next_frame()

def render_next_frame():
    SCREEN.fill(WHITE)
    draw_grid()
    draw_agents()
    pygame.display.update()
    FPSCLOCK.tick(60)

def draw_grid():
    # Draw horizontal lines
    y = 0
    while y < SCREEN_HEIGHT:
        start_pos = (0, y)
        end_pos = (SCREEN_WIDTH, y)
        pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
        y += 50

    # Draw vertical lines
    x = 0
    while x < SCREEN_WIDTH:
        start_pos = (x, 0)
        end_pos = (x, SCREEN_HEIGHT)
        pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
        x += 50

def draw_agents():
    for agent in agents:
        agent_rect = pygame.Rect(agent.x, agent.y, 50, 50)
        pygame.draw.rect(SCREEN, BLACK, agent_rect)

def main():
    run_simulation()

if __name__ == '__main__':
    main()