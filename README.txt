
---------------SOLAR SYSTEM SIMULATION (1000-YEAR ANALYSIS)---------------
Author: Nuno Zhan
Summary: A comparative numerical physics simulation of the solar system 
utilizing Beeman, Euler-Cromer, and Direct Euler integration methods.

1. INTRODUCTION
---------------
The Newtonian gravitational interactions of the solar system are 
simulated in this project. It is specifically designed to demonstrate 
the energy stability of the Beeman integrator over long timescales. 
Rare planetary alignment events are also identified and visualized.

2. INSTALLATION
---------------
Python 3.14.3 is used, along with the following libraries:
- NumPy  
- Matplotlib 
- SciPy (Utilized for circular statistics during alignment detection)

Dependencies may be installed via:
    pip install numpy matplotlib scipy

3. HOW TO RUN
-------------
Outputs include orbital animations, energy plots, and detected alignments.
-------------
A. DEFAULT BEEMAN RUN:
   > python Beeman_execution.py
   (The main simulation is executed with a dedicated energy stability plot).

B. PHYSICS COMPARISON:
   > python Comparison_execution.py
   (Beeman, Euler-Cromer, and Direct Euler are run side-by-side to 
   compare energy conservation and orbital animation).

C. PRIMARY ALIGNMENT SEARCH:
   > python Alignment_execution.py
   (The simulation runs for the full duration and identified 
   alignments are plotted. A 1-year cooldown is implemented to prevent 
   repeated captures of the same event, ensuring only distinct 
   alignments are recorded).

4. FILE DESCRIPTIONS
--------------------
--- CORE LOGIC ---
--> Simulation_Class.py   : The main engine used for simulation control, 
                          data loading, and alignment detection logic.
--> Body_Beeman.py        : The base celestial body and the Beeman 
                          integration algorithm are defined here.
--> Animator.py           : Interactive Matplotlib animations are handled 
                          with [Spacebar] pause/resume functionality.

--- INTEGRATION CASES --- (Via inheritance from the Beeman class)
--> Euler_Cromer_Case.py  : Implementation of the semi-implicit Euler.
--> Direct_Euler_Case.py  : Implementation of the non-conservative Euler.

--- CONFIGURATION ---
--> parameters_solar.json : Physical constants (Mass/Radius) for all bodies.
--> setting.json          : Timestep (0.005) and total duration settings. 
                          A range of 100 to 1000 years is recommended for 
                          optimal data, though longer tests are supported.

5. USER CONTROLS
----------------
- The animation may be paused or resumed by pressing [SPACEBAR].
- Detailed orbital period data (EY) is printed to the console 
  whenever the simulation is in a paused state.

--------------------------------------------------------------------------











