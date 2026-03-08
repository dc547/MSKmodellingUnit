"""KICKING SIMULATION

Iterates over activation levels, scales the rectus femoris column,
and creates new control files for each level.

Originally a MATLAB script by D. Cazzola, Uni of Bath
Python version
"""

import numpy as np
import pandas as pd

from CONTROLS.create_control_file import create_control_file


def main():
    # File paths (update to your local paths)
    xlsfile = 'EMGs.xlsx'
    template_control = 'controls_kick.xml'

    # Load example file
    df = pd.read_excel(xlsfile)
    txt = list(df.columns)
    num = df.values.copy()

    act = [0.1, 0.2, 0.3, 0.4]

    for activation in act:
        # Scale column index 1 (second column, first muscle) by activation
        new_RF = num[:, 1] * activation
        num[:, 1] = new_RF

        filename = f'new_control_{activation}.xml'

        create_control_file(num, template_control, filename, txt)
        print(f'Created {filename} with activation={activation}')


if __name__ == '__main__':
    main()
