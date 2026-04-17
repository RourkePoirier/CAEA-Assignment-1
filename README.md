# CAEA Assignment 1

## Project Overview

This repository contains two separate programs for finite element and mesh work:

1. **MATLAB Finite Element Analysis (FEA)**
   - Implemented in `Main.m`.
   - Reads `data_structure.xlsx` and performs a 2D triangular FEA solve.
   - Outputs displacement and stress results into Excel files.

2. **Python GUI Applications**
   - Implemented under `python_gui/mesh_generation` and `python_gui/visualisation`.
   - `python_gui\mesh_generation` provides a mesh generation editor for triangular meshes.
   - `python_gui\visualisation` provides a viewer for plotting and inspecting results.

## MATLAB Integration

The MATLAB program is the primary FEA solver in this project.

- Entry point: `Main.m`
- Input: `data_structure.xlsx`
- Outputs:
  - `displacement.xlsx`
  - `stress_x.xlsx`
  - `stress_y.xlsx`
  - `stress_xy.xlsx`

### Functionality

`Main.m` reads the input spreadsheet, assembles the global stiffness matrix, applies boundary conditions, solves for nodal displacements, and computes element stresses. It is designed for 2D triangular finite elements and uses hardcoded data positions in the spreadsheet.

### Running the MATLAB program

Open MATLAB or GNU Octave and run:

```matlab
Main
```

Make sure the current working folder contains `Main.m` and `data_structure.xlsx`.

## Python GUI Programs

There are two Python GUI applications in this repository.

### Mesh Generation GUI

- Path: `python_gui/mesh_generation`
- Entry point: `python_gui/mesh_generation/main.py`
- Purpose: create and edit triangular meshes, set node properties, and generate mesh geometry.

Run from the mesh generation folder:

```powershell
cd python_gui\mesh_generation
python main.py
```

### Visualisation GUI

- Path: `python_gui/visualisation`
- Entry point: `python_gui/visualisation/main.py`
- Purpose: display and visualise mesh data, results, and plots in a GUI window.

Run from the visualisation folder:

```powershell
cd python_gui\visualisation
python main.py
```

## Dependencies

### MATLAB

- MATLAB or GNU Octave for running `Main.m`.

### Python

The Python GUIs depend on the following libraries:

- `tkinter` (standard GUI toolkit in Python)
- `pandas`
- `numpy`
- `matplotlib`
- `scipy`

### Installation

Run start_program.mlapp in MATLAB

Press each button to launch the corrosponding stage of the program

## Notes

- This README only documents usage and dependencies.
- The MATLAB solver and Python GUIs are separate programs, so they can be used independently.

