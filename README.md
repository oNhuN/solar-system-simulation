# Solar System Simulation

A Python simulation of the Solar System designed to study long-term orbital behaviour and compare different numerical integration methods in an N-body gravitational system.

---

## Overview

This project simulates the Newtonian gravitational interactions between planets in the Solar System over long timescales (up to 1000 years).

The main focus of the project is comparing the stability and energy conservation of different numerical integration methods, particularly the Beeman integrator.

The simulation also includes:

- Orbital animations
- Energy conservation plots
- Comparison between integration methods
- Detection and visualization of planetary alignments

---

## Features

- Simulation of a chaotic multi-body gravitational system
- Comparison of:
  - Beeman Integration
  - Euler-Cromer Integration
  - Direct Euler Integration
- Long-term energy stability analysis
- Interactive animations
- Planetary alignment detection using circular statistics
- Pause and resume animation controls

---

## Requirements

Developed using **Python 3.14.3**

### Required Libraries

- NumPy
- Matplotlib
- SciPy

Install dependencies with:

```bash
pip install numpy matplotlib scipy
```

---

## How to Run

### A. Default Beeman Simulation

Runs the main simulation using the Beeman integrator and generates an energy stability plot.

```bash
python beeman_execution.py
```

---

### B. Integration Method Comparison

Runs Beeman, Euler-Cromer, and Direct Euler side-by-side to compare orbital behaviour and energy conservation.

```bash
python comparison_execution.py
```

---

### C. Planetary Alignment Detection

Runs the simulation and detects planetary alignment events.

A 1-year cooldown is used to prevent repeated captures of the same alignment.

```bash
python alignment_execution.py
```

---

## Project Structure

### Core Simulation Files

| File | Description |
|---|---|
| `Simulation_Class.py` | Main simulation engine and alignment detection logic |
| `Body_Beeman.py` | Celestial body class and Beeman integrator |
| `Animator.py` | Handles orbital animations and pause/resume controls |

---

### Alternative Integration Methods

| File | Description |
|---|---|
| `Euler_Cromer_Case.py` | Euler-Cromer integration method |
| `Direct_Euler_Case.py` | Direct Euler integration method |

---

### Configuration Files

| File | Description |
|---|---|
| `parameters_solar.json` | Physical parameters for celestial bodies |
| `setting.json` | Simulation timestep and duration settings |

---

## Simulation Settings

Default timestep:

```json
0.005
```

Recommended simulation duration:

- **100–1000 years**

Longer simulations are supported, although runtime increases significantly.

---

## Controls

| Key | Action |
|---|---|
| `SPACEBAR` | Pause / Resume animation |

---

## Notes

This project was created to investigate how different numerical integration methods behave over long timescales in gravitational systems.

The Beeman integrator shows much better long-term stability and energy conservation compared to standard Euler-based methods.

---

## Author

**Nuno Zhan**  
Physics Student — The University of Edinburgh
