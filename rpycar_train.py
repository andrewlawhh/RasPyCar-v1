import pickle
import neat
from simulation import Simulation
from simulation_config import *

'''
Summary: 
This script is intended to be a proof of concept for the RPyCar project.
Using NEAT, we will train a neural network using evolutionary computation, and after N generations, save the best
performing neural network.

Simulation:
The simulation should include
    1. A population of agents
    2. A waypoint
    3. Obstacles

The visuals for the simulation will be handled by simulation.py


PyGame configuration should be set up in a different file so all other classes can import that file and have access to
locations.

(Tentative) - Waypoint and Obstacle locations should be randomly generated in a different file, so the agent class has
access to it

Description of Evolution: 
Each agent receives input from its environment, passes it through its neural network, and receives instructions from
its neural network based on its output.
The end of each population is signaled when all agents have died (hit an obstacle) or reached the target.
Fitness is then calculated for each agent based on an inverse squared function of how close it got to the target.
The NEAT library will take care of repopulation and mutation of each subsequent generation.
Details of the evolutionary computations are abstracted away in the neat library, but parameters can be tweaked in the
config file.

After N generations, terminate the simulation and save the best performing neural network.
'''

# Driver for NEAT algorithm
def evolutionary_driver(n=NUM_GENERATIONS):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(False))

    # Run for n generations
    # p.run returns the best genome
    winner = p.run(eval_genomes, n = n)

    # save best genome to a file
    pickle.dump(winner, open('winner.pkl', 'wb'))
    print("Winner dumped into file")


# Args: list of genomes, NEAT configuration
# Return : None
# Run simulation for one generation and assign fitness scores to each genome at the end of the generation
def eval_genomes(genomes, config):
    print("evaluating genomes")
    # Run the simulation from simulation.py and collect results
    ids, genomes = zip(*genomes)
    genomes = list(genomes)
    sim = Simulation(genomes, config)
    sim.run_simulation()
    info = sim.finish_info

    # Calculate highest fitness and set fitness for each genome
    highest_fitness = 0
    lowest_distance = 1000000 # arbitrary high value
    lowest_steps = 1000000 # arbitrary high value

    # Info contains a list of tuples of (result, genome)
    # Result is a dictionary containing final distance to waypoint and steps it took to get there
    # Genome is the genome of the unit

    for tup in info:
        result, genome = tup

        # finishing distance to waypoint
        distance = result['distance']

        # manhattan distance from starting position to waypoint
        manhattan = result['manhattan']

        # number of steps taken
        steps = result['steps']

        # succeeded? (true/false)
        succeeded = result['succeeded']

        if succeeded:
            # Normalize steps so that random paths to close waypoints are not inadvertently rewarded
            normalized_steps = steps / manhattan
            # Flat reward for reaching the waypoint plus an inversed square law for steps taken to get there
            fitness = 100 + 1000 / (normalized_steps ** 2)
        else:
            # Fitness = inverse square of ending distance to waypoint
            fitness = 1 / (distance ** 2)

        # set genome.fitness to the calculated fitness
        genome.fitness = fitness

        if highest_fitness < fitness:
            highest_fitness = fitness

        if lowest_distance > distance:
            lowest_distance = distance

        if lowest_steps > steps:
            lowest_steps = steps

    # print metrics of the generation
    print('Highest Fitness :', highest_fitness)
    print('Lowest Distance :', lowest_distance)
    print('Lowest Steps :', lowest_steps)

def main():
    evolutionary_driver()

if __name__ == '__main__':
    main()