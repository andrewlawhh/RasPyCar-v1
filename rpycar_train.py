import pickle
import neat
from simulation import Simulation

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
def evolutionary_driver(n=50):
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
        print(tup)
        result, genome = tup
        distance = result['distance'] # dist to waypoint
        steps = result['steps'] # steps taken

        fitness = 1 / (distance ** 2) + 1 / (steps ** 2) # TODO - figure out some combination of distance and steps

        # set genome.fitness to the calculated fitness
        genome.fitness = -1 if fitness == 0 else fitness

        if highest_fitness < fitness:
            highest_fitness = fitness

        if lowest_distance > distance:
            lowest_distance = distance

        if lowest_steps > steps:
            lowest_steps = steps

    # print metrics of the generation
    print('Highest Fitness :', highest_fitness)
    print('Lowest Distance :', lowest_distance)

def main():
    evolutionary_driver()

if __name__ == '__main__':
    main()