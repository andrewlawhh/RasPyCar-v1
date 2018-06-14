import neat
import pickle
from simulation import Simulation

'''
In this file, we will load the best neural network from the training script and run it on a single agent.
This simulates porting the best neural network from the machine to the Raspberry Pi.
'''


def run_winner():
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # load genome
    genome = pickle.load(open('winner.pkl', 'rb'))

    sim = Simulation([genome], config)
    sim.run_simulation()


def main():
    run_winner()

if __name__ == '__main__':
    main()
