import matplotlib.pyplot as plt
from simulation_class import Simulation
from body_beeman import Beeman
from animator import MultiAnimator

def main():
    """Execution file for the default simulation (Beeman Method)"""
    sim = Simulation(body_type=Beeman)
    for b in sim.bodies.values():
        b.initializer(sim.dT, sim.bodies.values())
        b.sun = sim.bodies["sun"] # giving the sun mass (essential)
    
    sim.run_full_simulation()

    fig_en, ax_en = plt.subplots(figsize=(10, 5)) # energy plot
    sim.plot_energy(ax_en) 
    
    fig_anim, ax_anim = plt.subplots(figsize=(8, 8)) # animation plot
    animator = MultiAnimator([sim], fig_anim, [ax_anim])
     
    animator.run()
    plt.show()

if __name__ == "__main__":
    main()
