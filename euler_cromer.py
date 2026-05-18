from Body_Beeman import Beeman
from numpy.linalg import norm
class EulerCromer(Beeman):
    """
    Using inheritance to overwrite the Body class. 
    This method should conserve the energy but is not that accurate as the Beeman method.
    It uses a linear approximation and it assumes that the velocity and acceleration are constant during the timestep.
    
    """
    def initializer(self, dT, all_bodies):
        """Set up the self.a_current needed for calculations."""
        self.acceleration = self.calc_acceleration(all_bodies, self.position)

    def update_velocity(self, dT):
        """
        Firstly update the velocity 
        As the simulation class updates the position first and then the velocity, it is necessary to 
        reverse the order here. 
        As this function is updated firstly, it is possible to the velocity calculation here firstly.
        """
        self.acceleration = self.next_acc.copy()
        self.acceleration_list.append(norm(self.acceleration.copy())) # saving a history of acceleration easier to debug.
    def update_position(self, dT):
        """
        Using the updated velocity to calculate the updated position. 
        Parameters:
            - self.rel_p_previous: saving a copy of the previous for the calculation.
            - self.v update the velocity.
            - self.rel_p update position.
        """
        self.prev_position = self.position.copy()

        self.velocity += self.acceleration * dT # update velocity

        self.position += self.velocity * dT # update position
        
        self.position_history.append(self.position.copy())
        self.velocity_list.append(self.velocity.copy())
