from Body_Beeman import Beeman
from Simulation_Class import Simulation
import matplotlib.pyplot as plt
def main():
    """Execution file for the planetary alignment"""
    sim = Simulation(body_type=Beeman)
    for b in sim.bodies.values():
        b.initializer(sim.dT, sim.bodies.values())
        b.sun = sim.bodies["sun"]
    sim.run_full_simulation()
    sim.plot_alignment()
    plt.show()

if __name__ == "__main__":
    main()