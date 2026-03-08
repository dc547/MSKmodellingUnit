# MSK Modelling Unit - HL40064
<p align="right">
  <img src="docs/University_of_Bath_logo.svg.png" width="250" title="hover text">
</p>
This repository is created for HL40064 MSK modelling Unit students of the University of Bath.

You can find Matlab functions to create and modify .trc, .mot, and .sto data compatible with OpenSim 4.0. This functions can be be very useful to prepare the datasets and settings files to run procedures for your coursework.

## Python Versions

Python equivalents of all the MATLAB functions are also available in this branch. Each `.m` file has a corresponding `.py` file with the same name. The Python versions use the following libraries:

- **numpy** – numerical arrays and data handling
- **pandas** – reading Excel files (replaces MATLAB `xlsread`)
- **opensim** – OpenSim Python API (replaces MATLAB `import org.opensim.modeling.*`)
- **btk** – Biomechanical Toolkit Python bindings (for C3D file loading)
- **ezc3d** – reading/writing C3D files
- **scipy** – interpolation utilities

### File Mapping

| MATLAB File | Python File |
|---|---|
| `read_motionFile.m` | `read_motionFile.py` |
| `write_motionFile.m` | `write_motionFile.py` |
| `mot_creator.m` | `mot_creator.py` |
| `states_creator.m` | `states_creator.py` |
| `FD_prescribed.m` | `FD_prescribed.py` |
| `prescribeMotionInModel_customCoordinates.m` | `prescribeMotionInModel_customCoordinates.py` |
| `prescribe_and_simulate.m` | `prescribe_and_simulate.py` |
| `strengthScaler.m` | `strengthScaler.py` |
| `strengthScaler_AllMuscles.m` | `strengthScaler_AllMuscles.py` |
| `btk_loadc3d.m` | `btk_loadc3d.py` |
| `btk_sortc3d.m` | `btk_sortc3d.py` |
| `CONTROLS/xml2struct.m` | `CONTROLS/xml2struct.py` |
| `CONTROLS/struct2xml.m` | `CONTROLS/struct2xml.py` |
| `CONTROLS/create_control_file.m` | `CONTROLS/create_control_file.py` |
| `CONTROLS/RunFD_Diffcontrols.m` | `CONTROLS/RunFD_Diffcontrols.py` |
| `CONTROLS/kicking_sim.m` | `CONTROLS/kicking_sim.py` |
| `Data Handling/C3D_2_trc_mot.m` | `Data Handling/C3D_2_trc_mot.py` |
| `Data Handling/trc_mot_2_C3D.m` | `Data Handling/trc_mot_2_C3D.py` |
| `Data Handling/trc_refiner_v01.m` | `Data Handling/trc_refiner_v01.py` |
