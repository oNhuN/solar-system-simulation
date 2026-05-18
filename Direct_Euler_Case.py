from Body_Beeman import Beeman
from numpy.linalg import norm

class Direct_Euler (Beeman):
    """
    Inheriting from the Body class, changing the Physic engine of the problem
    Main difference with Euler_cromer is the order we are inputing the values.
    This follow the Beeman order while Cromer updates velocity first and after updates position
    Direct Euler is a numerical integration method which is not appropriate for this simulation
    as the energy would be loosing and there is not enough physics to simulate the planets orbit
    This method has a rever order physics from the Euler_Cromer by updating first the position and later the velocity.
    """
    
    def initializer(self, dT, all_bodies):
        """Initializing the self.a_current for the velocity update."""
        self.acceleration = self.calc_acceleration(all_bodies)
        

    def update_position(self, dT):
        """
        Updates the pos_position using the current position.
        self.rel_p = self.rel_p_previous (the reason of the copy() + ...)
        """
        self.prev_position = self.position.copy() # for next timestep calculation
        
        self.position += self.velocity * dT #formula

        self.position_history.append(self.position.copy())

        
    def update_velocity(self, dT):
        """
        Updates for the velocity using the updated position.
        """
        self.velocity += self.acceleration * dT #formula

        self.acceleration = self.next_acc.copy() # after calculating the current v we update the acceleration for the next timestep

        self.velocity_list.append(self.velocity.copy())
        self.acceleration_list.append(norm(self.acceleration.copy()))