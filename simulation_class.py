import numpy as np 
from numpy.linalg import norm  # giving linera algebra calculations
import matplotlib.pyplot as plt
import json
from scipy.stats import circmean
class Simulation:

    def __init__(self, body_type):
        """
        Read in json files and description of constants and objects.
        Parameters:
            - self.raw_data: contains the information read from the data.
            - self.bodies: Stored all the information in the bodies (planets)
            - self.dT: timestep read from json file
            - self.total_years: total time that the simulation will run
            - self.patches: list of diccionary to store the updated patches.
            - self.is_paused: boolean for key pressing.
            - self.kinetic_list, self.potential_list, self.orbital_list for plotting.
        """
        self.body_type = body_type # to check which method we are using for the simulation
        self.current_frame = 0
        
        # load settings
        with open("setting.json", "r") as h: # loading timestep from json.
            config = json.load(h)
        self.dT = config["setting"]["timestep"]
        self.total_years = config["setting"]["total_years"]
        self.G = config["setting"]["G"]

        # load bodies
        with open("parameters_solar.json", "r") as f:
            parameter_solar = json.load(f)["bodies"]
        # load sun_mass 
        sun_mass = next(
            b["mass"] for b in parameter_solar
            if b["name"].lower() == "sun"
            )

        self.raw_data = [self.body_type(**item, G = self.G, sun_mass = sun_mass) for item in parameter_solar] # this will iterate through all the bodies
        self.bodies =  {b.name: b for b in self.raw_data}
        
        self.time_simulated = int(self.total_years/self.dT) # total times that the simulation is being run
        self.patches = {} # open a list of dicctionary
        self.is_paused = False # for pressing key
        
        self.kinetic_list = []
        self.potential_list = []
        self.orbital_list = []


    def step_forward(self): 
        
        """
        Executes a single time step of the simulation by updating the data for each body.
        Coordinates a three-pass iteration over all bodies to ensure time-consistency:
        1. Position Update: Advances all coordinates to t + dT
        2. Force Evaluation: Calculates new accelerations based on the updated positions.
        3. Velocity Correction: Finalizes the state update and computes system-wide 
        kinematics, including energy conservation (KE/PE) and orbital metrics.

        Synchronizes the global simulation state by preventing bodies from 
        updating based on partially-advanced neighbor positions.
        """
        self.total_KE = 0.0
        self.total_PE = 0.0
        for k,v in self.bodies.items():
            v.update_position(self.dT) #update in the first loop the position so that we can use it to calculate the acc_next
        
        for k,v in self.bodies.items(): # update the acceleration so that each body has the new update
            v.next_acc = v.calc_acceleration(self.bodies.values()) # we store in v the next_acc based on the position update
            
        for k, v in self.bodies.items(): # passing the new acceleration as an argument
            v.update_velocity(self.dT)

            self.total_KE += v.calc_KE()
            self.total_PE += v.calc_PE(self.bodies.values())

            v.check_orbital_period(self.dT)
            self.orbital_list.append(v.orbital_count)

        self.kinetic_list.append(self.total_KE)
        self.potential_list.append(self.total_PE)

    def run_full_simulation(self):
        """
        Running the whole simulation before the animation plotting.
        """
        print(f"-----Completed Simulation Data: {self.body_type.__name__}-----")
        
        for i in range(self.time_simulated):
            self.step_forward()
        
        for k, v in self.bodies.items(): # printing out the data of the whole simulation
            if k.lower() == "sun":
                continue
            else:
                print(f"{k.capitalize()} total orbits = {v.orbital_count}")

    def display(self, fig, ax):
        """
        Initialize the circular patches for each body. Configuration of the plot and limits based
        on the maximum orbital radius and customization of radial grid for better visualization.
        """
        total_frames = max(len(v.position_history) for v in self.bodies.values())

        plt.style.use('dark_background')
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        max_radius = 0
        for k, v in self.bodies.items():
            if v.orbital_radius > max_radius:
                max_radius = v.orbital_radius

            p = plt.Circle((v.position_history[0][0],
                            v.position_history[0][1]),
                            0.1,
                            color=v.colour,
                            animated=True)

            self.patches[k] = p
            ax.add_patch(p)

        ax.axis('scaled')

        limit = max_radius * 1.2 if max_radius > 0 else 5.0 # setting up the limits

        grid_color = '#6ec6ff'
        # plotting customization
        for angle in np.linspace(0, 2*np.pi, 12):
            ax.plot([0, np.cos(angle)*limit], [0, np.sin(angle)*limit], color=grid_color, alpha=0.2, linewidth=0.5)

        for r in np.linspace(limit/10, limit, 8):
            circle = plt.Circle((0, 0), r,
                                color=grid_color,
                                fill=False,
                                alpha=0.2,
                                linewidth=0.5)
            ax.add_artist(circle)

        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_title(f"{self.body_type.__name__}", color='white')
        ax.tick_params(colors='white')

        return total_frames
    
    def planet_alignment(self):
        """
        Detects planetary alignment events over the simulation.
        At each timestep, the angular positions of all planets relative to sun are computed and 
        compared to their circular mean angle. Alignment is defined as all planets being within a 
        specific angular threshold of this mean direction. This will occur more frequently 
        depending on the angular threshold.
        """
        alignment_steps = []
        is_aligned = False
        threshold = np.radians(10)
        skip = int(2.0 / self.dT)
        sun = self.bodies["sun"]  # or however your Sun key is cased

        for i in range(skip, self.time_simulated):
            sun_pos = np.array(sun.position_history[i])
            
            angles_rad = np.array([
                np.arctan2(
                    v.position_history[i][1] - sun_pos[1],  # relative to Sun
                    v.position_history[i][0] - sun_pos[0]
                        )   
                for k, v in self.bodies.items()
                if k.lower() != "sun"
            ])

            mean_angle = circmean(angles_rad, low=-np.pi, high=np.pi)
            gaps = np.arctan2(
                np.sin(angles_rad - mean_angle),
                np.cos(angles_rad - mean_angle)
            )

            currently_aligned = np.all(np.abs(gaps) < threshold)
            if currently_aligned and not is_aligned:
                alignment_steps.append(i)
            is_aligned = currently_aligned

        return alignment_steps
        
    def plot_alignment(self):
        """
        Plot picture of the specific moment of a planetary alignment.
        For each plot, the position of the planets are relative to the sun (fixed at the origin)
        for a clear visualization alignment. 
        """
        steps = self.planet_alignment()
        if not steps:
            print("No alignment found")
            return 

        sun = self.bodies["sun"]
        max_radius = max(v.orbital_radius for k, v in self.bodies.items() if k.lower() != "sun")
        limit = max_radius * 1.5 if max_radius > 0 else 5.0
        grid_color = "#6ec3fc"

        for step in steps:
            plt.figure(figsize=(8, 8))
            plt.style.use('dark_background')
            ax = plt.gca()
            ax.set_facecolor('black')
            plt.gcf().patch.set_facecolor('black')

            # Get the actual position of the sun at this timestep
            sun_pos = np.array(sun.position_history[step])

            for k, v in self.bodies.items():
                if k.lower() == "sun": continue
                pos = np.array(v.position_history[step])
                # Plot relative to sun
                rel = pos - sun_pos
                ax.scatter(rel[0], rel[1],
                           color=v.colour,
                           edgecolor='white',
                           linewidth=0.5,
                           label=k)

            # Sun always at centre (for better visualization), customization
            ax.scatter(0, 0, color='yellow', edgecolor='orange', linewidth=1.2, label='Sun')

            for angle in np.linspace(0, 2*np.pi, 12):
                ax.plot([0, np.cos(angle)*limit], [0, np.sin(angle)*limit], color=grid_color, alpha=0.2, linewidth=0.5)

            for r in np.linspace(limit/10, limit, 8):
                circle = plt.Circle((0, 0), r, color=grid_color, fill=False, alpha=0.2, linewidth=0.5)
                ax.add_artist(circle)

            ax.set_xlabel("x (AU)", color='white')
            ax.set_ylabel("y (AU)", color='white')
            ax.set_title(f"Alignment at t = {step * self.dT:.2f} years", color='white')
            ax.tick_params(colors='white')
            ax.set_aspect('equal', adjustable='box')
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.legend()
            plt.show()


    def plot_acceleration(self, ax):    
        """ Acceleration plotting """
        for k, v in self.bodies.items():
            if k.lower() == "sun": continue
            y = v.acceleration_list
            x = [i * self.dT for i in range(len(y))]
            ax.plot(x, y, label=k, color=v.colour)
        ax.set_xlabel("Time (Years)")
        ax.set_ylabel("Acceleration Magnitude")
        ax.set_title(f"{self.body_type.__name__} Acceleration")
        ax.legend()
        ax.grid(True)
            
    def plot_energy(self, ax):
        """Total energy plotting"""
        kinetic_energy = np.array(self.kinetic_list)
        potential_energy = np.array(self.potential_list)
        self.total_energy = kinetic_energy + potential_energy

        time_axisTE = [i * self.dT for i in range(len(self.total_energy))]
        ax.plot(time_axisTE, self.total_energy, color = 'blue')
        # Total Energy
        ax.set_xlabel("Time (Years)")
        ax.set_ylabel("Total Energy")
        ax.set_title(f"{self.body_type.__name__} Energy")
        ax.grid(True)

        plt.tight_layout()
        
        

 
  
