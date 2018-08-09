# Proof of Concept Software for Autonomous Vehicle
This is an example of the NEAT algorithm in action. Over several generations, agents will become better at locating a randomized target without using search algorithms.

### Customizing Settings
Settings for the evolutionary algorithm can be changed in the config text file; documentation for the neat-python library can be found [here](https://neat-python.readthedocs.io/en/latest/).

Settings for the simulation, such as number of agents, location of targets, and number of generations can be changed in the sim_config.py file.

### Training the model
Run the rpycar_train.py file to start the simulation. Metrics are printed out in the console after each generation to better monitor the simulation.

After the simulation is complete, a .pkl file containing the best performing neural network is dumped into the directory. Running rpycar_runbest.py will load this into a new simulation to be run for one generation, so the user can better examine the results of the model.

