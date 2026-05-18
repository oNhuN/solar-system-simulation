from body_beeman import Beeman
from simulation_class import Simulation
from direct_euler import Direct_Euler
from euler_cromer import EulerCromer
import matplotlib.pyplot as plt
from animator import MultiAnimator

def main():
    """
    Execution file to compare all three methods of numerical integration.
    It includes the following graphs for all three simulations:
        - Animation plot
        - Total energy plot 
        - Acceleration plot
    """ 

    physics_methods = [Beeman, EulerCromer, Direct_Euler]
    completed_simulations = []
    
    for case in physics_methods: 
        sim = Simulation(body_type=case)
        for b in sim.bodies.values():
            b.initializer(sim.dT, sim.bodies.values()) 
            b.sun = sim.bodies["sun"]
        sim.run_full_simulation()
        
        completed_simulations.append(sim)

    fig_energy, axes_energy = plt.subplots(3, 1, figsize=(12, 12))
    fig_acc, axes_acc = plt.subplots(1, 3, figsize = (15, 5))
    for n in range(len(completed_simulations)):

        completed_simulations[n].plot_energy(axes_energy[n])
        completed_simulations[n].plot_acceleration(axes_acc[n])
        
    fig_anim, axes_anim = plt.subplots(1, 3, figsize=(12, 4))
    animator = MultiAnimator(completed_simulations, fig_anim, axes_anim)
    animator.run()
    print(f"Sun final position (Beeman): {completed_simulations[0].bodies['sun'].position}")

    fig_energy.tight_layout() 
    fig_acc.tight_layout()
    fig_anim.tight_layout()  
    plt.show()

if __name__ == "__main__":
    main()

