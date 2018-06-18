import neat
import random
import simulation_config as sim_cfg

dir_list = ['up', 'right', 'down', 'left']
class Unit:

    def __init__(self, genome, config):

        # Initialize unit status
        self.dead = False
        self.reached_waypoint = False

        # Initialize unit position
        self.x_pos = sim_cfg.AGENT_INITIAL_X
        self.y_pos = sim_cfg.AGENT_INITIAL_Y

        # Initialize obstacles reference
        self.obstacles = sim_cfg.OBSTACLES

        # Initialize waypoint reference
        self.waypoint = sim_cfg.WAYPOINT

        # Initialize previous waypoint distances
        self.waypoint_dist_x_prev = self.waypoint_dist_x()
        self.waypoint_dist_y_prev = self.waypoint_dist_y()

        # Initialize starting manhattan distance
        self.starting_manhattan_distance = self.waypoint_manhattan_dist()

        # Set instance variable to save steps taken
        self.steps = 0

        # Set instance variable to save distance to waypoint
        self.dist_to_waypoint = None

        # Initialize genome reference
        self.genome = genome

        # Initialize direction in degrees
        self.direction = 0 # Math.PI / 2

        # Previous direction
        self.direction_prev = 0

        # Initialize unit neural network
        self.neural_network = neat.nn.RecurrentNetwork.create(genome, config)

        # Initialize termination information
        self.finish_info = ()

    '''
    Movement methods
    '''

    # Pass input through neural network and get move
    # Args : None | Returns : Int corresponding to move
    def get_move(self):
        # Inputs to be fed into the neural network
        input = [self.waypoint_dist_x(),
                 self.waypoint_dist_y(),
                 self.direction]

        # Normalization function for inputs to be converted to values in range [-1, 1]
        def normalize(tpl):
            l = list(tpl)
            maximum = max([abs(x) for x in l])
            normalized_l = [x/maximum for x in l]
            return tuple(normalized_l)

        # Normalize inputs
        input = normalize(input)

        # Get output from neural network
        output = self.neural_network.activate(input)

        def prob_based():
            output_sum = sum(output)
            running_sum = 0
            rando = random.uniform(0, output_sum)
            for i in range(len(output)):
                running_sum += output[i]
                if running_sum > rando:
                    return i

        def max_based():
            return output.index(max(output))

        return max_based()

    # Move unit
    # Args : None | Returns : None
    def move(self):
        # Get move command (0, 1, 2, 3) from self.get_move()
        # 0 : Forward
        # 1 : Left
        # 2 : Right
        # 3 : Stop
        move_command = self.get_move()

        # Implemented in this manner so that we can change what each command does
        if move_command == 0:
            self.move_forward()
        if move_command == 1:
            self.turn_left()
        if move_command == 2:
            self.turn_right()
        if move_command == 3:
            self.stop()
        self.steps += 1

    # Move forward command
    # Args : None | Returns : None
    def move_forward(self):
        #print(self.genome.key, 'moved forward')
        if dir_list[self.direction] == 'right':
            self.x_pos += sim_cfg.UNIT_SIZE
        if dir_list[self.direction] == 'up':
            self.y_pos -= sim_cfg.UNIT_SIZE
        if dir_list[self.direction] == 'left':
            self.x_pos -= sim_cfg.UNIT_SIZE
        if dir_list[self.direction] == 'down':
            self.y_pos += sim_cfg.UNIT_SIZE

    # Turn left command
    # Args : None | Returns : None
    def turn_left(self):
        #print(self.genome.key, 'turned left')
        self.direction = (self.direction - 1) % 4
        #self.move_forward()

    # Turn right command
    # Args : None | Returns : None
    def turn_right(self):
        #print(self.genome.key, 'turned right')
        self.direction = (self.direction + 1) % 4
        #self.move_forward()

    # Stop command
    # Args : None | Returns : None
    def stop(self):
        # Do nothing
        print(self.genome.key, 'stopped')
        pass

    # Updates unit. (Move, but with checks to see if the unit has died or reached goal)
    # Args : None | Returns : None
    def update(self):
        # If unit is alive and has not reached the waypoint, check status and move
        # Check is performed twice so that upon death or success, the unit is not immediately moved
        if not self.dead and not self.reached_waypoint:
            self.check_dead()
            self.check_reached_waypoint()

            # Check to make sure the agent does not move immediately after it has died or reached the waypoint
            if not self.dead and not self.reached_waypoint:
                self.move()

    '''
    Distance measurement methods
    '''

    # Returns distance between two points
    # Args : x1 coord, y1 coord, x2 coord, y2 coord | Returns : float
    def dist(self, x1, y1, x2, y2):
        return ( ((x1 - x2) ** 2) + ((y1 - y2) ** 2) ) ** 0.5

    # Returns distance from agent to waypoint
    # Args : None | Returns : double (distance to waypoint)
    def waypoint_dist(self):
        return self.dist(self.x_pos, self.y_pos, self.waypoint.x_pos, self.waypoint.y_pos) // sim_cfg.UNIT_SIZE

    # Returns x distance from waypoint
    def waypoint_dist_x(self):
        return (self.waypoint.x_pos - self.x_pos) // sim_cfg.UNIT_SIZE

    # Returns y distance from waypoint
    def waypoint_dist_y(self):
        return (self.waypoint.y_pos - self.y_pos) // sim_cfg.UNIT_SIZE

    def waypoint_manhattan_dist(self):
        return (abs(self.waypoint_dist_x()) + abs(self.waypoint_dist_y()))


    '''
    Status checking methods
    '''

    # Checks if unit has crashed and assigns correct boolean to instance attribute
    # If it is dead, assign crash info to instance variable to be passed to simulation.py
    # Make sure the assignment happens only ONCE, when the unit has just died.
    # Args : None | Returns : None
    def check_dead(self):
        # Die if unit crashed into an obstacle
        for obstacle in self.obstacles:
            if obstacle.x_pos <= self.x_pos < obstacle.x_pos + obstacle.width and \
                obstacle.y_pos <= self.y_pos < obstacle.y_pos + obstacle.height:
                self.die()
        # Die if unit is not within borders of the simulation
        if self.x_pos <= 0 or self.x_pos >= sim_cfg.SCREEN_WIDTH - sim_cfg.UNIT_SIZE or self.y_pos <= 0 or self.y_pos >= sim_cfg.SCREEN_HEIGHT - sim_cfg.UNIT_SIZE:
            self.die()
        # Die if unit is taking too long to reach the waypoint
        # This prevents the unit from spinning in circles
        if self.steps > 150:
            self.die()

    # Checks if unit has reached waypoint and assigns correct boolean to instance attribute
    # If it has reached the waypoint, assign termination info to instance variable to be passed to simulation.py
    # Make sure the assignment happens only ONCE, when the unit has just reached the waypoint.
    # Args : None | Returns : None
    def check_reached_waypoint(self):
        if self.waypoint_dist() == 0:
            self.succeed()

    '''
    Termination methods
    '''

    # Method called to kill the unit
    def die(self):
        self.dead = True
        self.set_finish_info()

    # Method called if the unit reaches the waypoint
    def succeed(self):
        self.reached_waypoint = True
        self.set_finish_info()

    # Populate finish info with the tuple of (dictionary (result) , genome)
    def set_finish_info(self):
        self.finish_info = {'distance': self.waypoint_dist(),
                            'steps': self.steps,
                            'succeeded' : self.reached_waypoint,
                            'manhattan' : self.starting_manhattan_distance},\
                           self.genome

    '''
    Methods that take inputs from the environment
    '''

    # Return reading from left sensor
    # Args : None | Returns : double (distance)
    def get_input1(self):
        scan_dir = self.direction + 90
        return random.randint(1, 3)

    # Return reading from left+forward sensor
    # Args : None | Returns : double (distance)
    def get_input2(self):
        return random.randint(1,3)

    # Return reading from forward sensor
    # Args : None | Returns : double (distance)
    def get_input3(self):
        return random.randint(1,3)

    # Return reading from right+forward sensor
    # Args : None | Returns : double (distance)
    def get_input4(self):
        return random.randint(1,3)

    # Return reading from right sensor
    # Args : None | Returns : double (distance)
    def get_input5(self):
        return random.randint(1,3)
