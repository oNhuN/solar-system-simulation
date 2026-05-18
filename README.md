# Solar System Simulation
This is a simulation written in Python about a chaotic N-body system. 

---

### SOLAR SYSTEM SIMULATION (1000-YEAR ANALYSIS)
* **Author:** Nuno Zhan
* **Summary:** A comparative numerical physics simulation of the solar system utilizing Beeman, Euler-Cromer, and Direct Euler integration methods.

---

## 1. Introduction
The Newtonian gravitational interactions of the solar system are simulated in this project. It is specifically designed to demonstrate the energy stability of the Beeman integrator over long timescales. Rare planetary alignment events are also identified and visualized.

## 2. Installation
Python 3.14.3 is used, along with the following libraries:
* **NumPy**
* **Matplotlib**
* **SciPy** *(Utilized for circular statistics during alignment detection)*

Dependencies may be installed via terminal using:
```bash
pip install numpy matplotlib scipy
```
3. How to Run
Outputs include orbital animations, energy plots, and detected alignments.
A. Default Beeman Run
The main simulation is executed with a dedicated energy stability plot:
```bash
python Beeman_execution.py
```
B. Physics Comparison
Beeman, Euler-Cromer, and Direct Euler are run side-by-side to compare energy conservation and orbital animation:
```bash
python Comparison_execution.py
```
C. Primary Alignment Search
The simulation runs for the full duration and identified alignments are plotted. A 1-year cooldown is implemented to prevent repeated captures of the same event, ensuring only distinct alignments are recorded:
```bash
python Alignment_execution.py
```
4. File Descriptions
Core Logic
Simulation_Class.py: The main engine used for simulation control, data loading, and alignment detection logic.

Body_Beeman.py: The base celestial body and the Beeman integration algorithm are defined here.

Animator.py: Interactive Matplotlib animations are handled with [Spacebar] pause/resume functionality.

Integration Cases (Via inheritance from the Beeman class)
Euler_Cromer_Case.py: Implementation of the semi-implicit Euler method.

Direct_Euler_Case.py: Implementation of the non-conservative Euler method.

Configuration
parameters_solar.json: Physical constants (Mass/Radius) for all celestial bodies.

setting.json: Timestep (0.005) and total duration settings. A range of 100 to 1000 years is recommended for optimal data, though longer tests are supported.

5. User Controls
The animation may be paused or resumed by pressing [SPACEBAR].

Detailed orbital period data (EY) is printed to the console whenever the simulation is in a paused state.
