import numpy as np 
from numpy.linalg import norm  # giving linera algebra calculations

class Beeman:
    """Body class that performs the physics of the simulation (Beeman method)"""

    
    def __init__(self, name, mass, orbital_radius, colour, G, sun_mass):
        """
        Setting up the initial conditions needed for the simulation.
        The units are in AU, Earth Years and Earth masses.
        Parameters:
            - self.name; self.mass; self.orbital_radius; self.colour:
                - read from the json.
            - self.velocity; self.position; self.acceleration; self.a_previous all in numpy arrays to facilitate calculation
            - self.initial_kinetic; self.initial_potential for storing the energies.
                - these will return floats telling us the energies in each
            - self.position_history; self.velocity_list used to store the updates that will be shown in the plot.
        """
        self.name = name
        self.mass = mass
        self.orbital_radius = orbital_radius
        self.colour = colour    
        self.G = G
        self.sun_mass = sun_mass

        self.etime_lastorbit = 0.0
        self.orbital_count = 0.0
        self.lastperiod = []
        self.timelist = []
        self.acceleration = np.zeros(2)
        self.a_previous = np.zeros(2)
        
        if self.name.lower() == "sun":
            self.velocity = np.array([0.0, 0.0])
            self.position = np.array([0.0, 0.0])
        else:
            self.v_mag = np.sqrt(((self.G * sun_mass)/self.orbital_radius))  # *1.1 will break the perfect ballance
            self.position = np.array([self.orbital_radius, 0.0])
            self.velocity = np.array([0.0, self.v_mag])


        self.initial_kinetic = 0.5 * self.mass * (np.linalg.norm(self.velocity)) ** 2
            
        self.acceleration_list = []
        self.position_history = [self.position.copy()]
        self.velocity_list = [self.velocity.copy()]
    
    def initializer(self, dT, all_bodies):
        """
        Sets the initial state for the Beeman integration method.

        The Beeman algorithm is a multi-step method that requires the acceleration 
        from the previous timestep a(-dT) to calculate the next 
        position and velocity. This method performs a back-extrapolation to 
        estimate that prior state.

        Args:
            dT (float): The time step size.
            all_bodies (list): A list of all body objects in the simulation 
                used to calculate gravitational/force interactions.

        Updates:
            self.acceleration: Sets the acceleration at the start time ($t=0$).
            self.prev_position: Estimates the position at -dT
            self.a_previous: Estimates the acceleration at -dT
        """
        self.acceleration = self.calc_acceleration(all_bodies, self.position) 

        prev_position = self.position - self.velocity * dT + (0.5 * self.acceleration*(dT**2)) #previous step from the beginning
        self.prev_position = prev_position

        self.a_previous = self.calc_acceleration(all_bodies, self.prev_position) # back-extrapolated 
        
    def update_position(self, dT):
        """
        Updates position using the Beeman integration scheme:
        """
        self.prev_position = self.position.copy() # needing the previous to calculate the following timestep. 
        #self.position (for next dT) = self.position (in fact self.prev_position) + ...
        
        self.position += self.velocity * dT + (1/6) * (4*self.acceleration - self.a_previous) * (dT**2)
        self.position_history.append(self.position.copy())

    def update_velocity(self, dT):
        """
        Updates velocity using the Beeman method and shifts acceleration states.

        Uses the newly calculated next acceleration next_acc, current self.acceleration, 
        and previous self.a_previous states to update velocity, then advances the 
        acceleration history for the next time step.
        """
        self.velocity += (1/6) * (2*self.next_acc + 5*self.acceleration - self.a_previous) * dT 

        self.a_previous = self.acceleration.copy() # update the acceleration to prevent acceleration summing up.
        self.acceleration = self.next_acc.copy()

        self.acceleration_list.append(norm(self.acceleration))
        self.velocity_list.append(self.velocity.copy())

    def calc_acceleration(self, bodies, position = None):
        """
        Computes the net gravitational acceleration vector exerted on this body.

        Calculates the vector sum of gravitational interactions from all other bodies 
        in the system using Newton's law of universal gravitation. Supports an optional 
        position override (position) to evaluate acceleration at predicted coordinates 
        without modifying the body's actual state.

        Args:
            bodies: A collection of objects with mass and position attributes.
            posiiton: vector needed for the calculation
                If None, uses the body's current position.
        Returns:
            A 2D numpy array representing the net acceleration vector [ax, ay].
        """
        if position is None: # make position optional, even it still takes position
            position = self.position
        
        acc = np.zeros(2)
        for other in bodies:
            if other is self: # skip the case whenever bodies match up
                continue
            r_vec = other.position - position #rji vector 
            dist = np.linalg.norm(r_vec)
            if dist == 0:
                continue
            acc += (self.G * other.mass * r_vec) / (dist**3)           
        return acc


    def calc_KE(self):
        """Calculates the kinetic energy of each body."""
        kinetic_e = 0.5 * self.mass * (np.linalg.norm(self.velocity))**2
        return kinetic_e

    def calc_PE(self, all_bodies):
        """Computes gravitational potential energy using pairwise interactions and the factor 1/2 prevents double counting"""
        potential = 0.0
        for other in all_bodies:
            if other is self:
                continue
            r_vec = other.position - self.position
            dist = np.linalg.norm(r_vec)
            if dist == 0: # avoid zero division
                continue
            potential += -0.5 * (self.G * other.mass * self.mass)/ dist # factor of 0.5 to prevent the double-counting pairs when summing the total energy of the system
                                                                          # in the simuation class loop
        return potential
       
    def check_orbital_period(self, dT):
        """Checking planets orbits whenever is completed relative to sun as this will drift over time due to gravitational pull of the planets (recording down the timestep)"""
        self.etime_lastorbit += dT # for last orbit calculation
        
        rel_y_prev = self.prev_position[1] - self.sun.prev_position[1]
        rel_y_curr = self.position[1] - self.sun.position[1]

        if rel_y_prev < 0 and rel_y_curr >= 0: # condition whenever y pass from negative to positive
            
            self.lastperiod.append(self.etime_lastorbit) # typing out the period of the last 
            self.timelist.append(sum(self.lastperiod))
            self.orbital_count +=1 # for the total orbit
            self.etime_lastorbit = 0
