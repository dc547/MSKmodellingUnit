import numpy as np
import pandas as pd
import warnings

from read_motionFile import read_motionFile
from write_motionFile import write_motionFile


def states_creator(states_example_file, states_file, states_output_file):
    """
    Load states file created via FD.

    INPUTS

    (1) states_example_file - (string) - This is the filename of the .sto
        file that is coming from an OpenSim FD output

    (2) states_file - (string or numpy array) - Filename of the .xls file
        you have manually changed in Excel, or a numpy array directly

    (3) states_output_file - (string) - Filename for the new .sto file
        created with this function

    Originally written by D. Cazzola, Uni of Bath, 10/11/2020
    """

    ## Load excel file
    if isinstance(states_file, str):
        num = pd.read_excel(states_file, header=None).to_numpy(dtype=float)
        row = num.shape[0]
    else:
        num = np.asarray(states_file, dtype=float)
        row = num.shape[0]

    ## Load states example
    sto = read_motionFile(states_example_file)

    ## Check compatibility
    if num.shape[1] != sto.data.shape[1]:
        warnings.warn(
            'The number of states is incorrect. Check both sto_example and the input file.'
        )
        return

    # Just get the first line for the initial conditions
    if row == 1:
        data = num  # check that the time is in line with other file inputted in the FD
        print('States to be used as initial conditions for FD')
    else:
        data = num[0:1, :]
        warnings.warn('States present for more than one frame - Correct?')

    ## Write states
    sto.data[0, 1:] = data[0, 1:]  # time starts at 0 now
    sto.data = sto.data[0:1, :]
    write_motionFile(sto, states_output_file)
