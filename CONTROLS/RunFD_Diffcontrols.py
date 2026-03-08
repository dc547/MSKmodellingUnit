"""Example with data changed programmatically in Python.

Runs multiple forward dynamics simulations with varying activation levels.

Originally a MATLAB script by D. Cazzola, Uni of Bath
Python version
"""

import numpy as np
import pandas as pd

from CONTROLS.create_control_file import create_control_file

# Requires: import opensim  (uncomment when opensim Python bindings are available)


def main():
    # File paths (update to your local paths)
    xlsfile = 'EMGs.xlsx'
    osimModel_file = 'SoccerKickingModel.osim'

    # Read excel file
    df = pd.read_excel(xlsfile)
    txt = list(df.columns)
    num = df.values
    row, col = num.shape
    time = num[:, 0]

    n_sims = 50

    # Create a 3D array of zeros: (row, col-1, n_sims)
    base_EMGs = np.zeros((row, col - 1, n_sims))

    for j in range(n_sims):
        dec_factor = (j + 1) / 100.0

        activation_coeff = np.ones(col - 1) * dec_factor
        base_EMGs[:, :, j] = num[:, 1:] * activation_coeff

        # Build control data with time as first column
        control_data = np.column_stack([time, base_EMGs[:, :, j]])

        create_control_file(
            control_data,
            'controls_kick.xml',
            f'new_control_{j + 1}.xml',
            txt
        )

        # --- Run Forward Dynamics ---
        # Uncomment the following when opensim Python bindings are available:
        #
        # import opensim
        # f_time = time[-1]
        # osimModel = opensim.Model(osimModel_file)
        #
        # ft = opensim.ForwardTool()
        # ft.setModel(osimModel)
        # ft.setSolveForEquilibrium(True)
        # ft.setErrorTolerance(1e-7)
        # ft.setMaxDT(time[1] / 100.0)
        # ft.setMinDT(time[1] / 1000.0)
        # ft.setInitialTime(0)
        # ft.setFinalTime(f_time)
        # ft.setName(f'new_res_{j + 1}.sto')
        # ft.run()

        print(f'Simulation {j + 1}/{n_sims} complete (dec_factor={dec_factor:.2f})')


if __name__ == '__main__':
    main()
