import numpy as np
import pandas as pd
import re
import warnings

from read_motionFile import read_motionFile
from write_motionFile import write_motionFile


def mot_creator(mot_example, input_file, mot_new_name, file_type):
    """
    Modify .mot file from .xls or numpy matrix.

    This can be used to modify both kinematics and kinetics .mot files.

    Parameters
    ----------
    mot_example : str
        Filename of the .mot file you want to modify.
    input_file : str or numpy.ndarray
        Filename of the Excel file including the new data, or a numpy array
        including data (with time as the first column).
    mot_new_name : str
        Filename for the new .mot file created.
    file_type : str
        Options: 'FD' - .mot example from forward dynamics;
                 'IK' - .mot from IK;
                 'LO' - .mot for creating external load file.

    Originally written by D. Cazzola, Uni of Bath, 10/11/2020
    """

    ## Read motion file
    data_temp = read_motionFile(mot_example)

    if isinstance(input_file, str):
        ## Import digitised points from .xls
        df = pd.read_excel(input_file, header=None)
        num = df.to_numpy(dtype=float)
        row = num.shape[0]

        # Get the time, which should be the first column in the .xls file
        time = num[:, 0]

        if num.shape[1] != data_temp.data.shape[1]:
            warnings.warn(
                'The number of states or external load is incorrect. '
                'If you are not using a file from FD you need to check your inputs!'
            )
    else:
        # Expecting a matrix with time as first column and then data
        num = np.asarray(input_file)
        row = num.shape[0]
        time = num[:, 0]

    ## CASES for the input file
    if file_type == 'FD':
        print('%%%% FD file %%%%')

        # Remove columns containing 'speed'
        indices_to_remove = [
            i for i, label in enumerate(data_temp.labels)
            if 'speed' in label
        ]
        data_temp.labels = [
            label for i, label in enumerate(data_temp.labels)
            if i not in indices_to_remove
        ]
        data_temp.data = np.delete(data_temp.data, indices_to_remove, axis=1)

        # Remove columns containing 'forceset'
        indices_to_remove = [
            i for i, label in enumerate(data_temp.labels)
            if 'forceset' in label
        ]
        data_temp.labels = [
            label for i, label in enumerate(data_temp.labels)
            if i not in indices_to_remove
        ]
        data_temp.data = np.delete(data_temp.data, indices_to_remove, axis=1)

        for i in range(len(data_temp.labels)):
            if data_temp.labels[i] and 'time' not in data_temp.labels[i]:
                s = data_temp.labels[i]
                # Replicate MATLAB logic:
                # ns_1 = erase(str, "/jointset/")
                ns_1 = s.replace('/jointset/', '')
                # ns_2 = erase(ns_1, "/value")
                ns_2 = ns_1.replace('/value', '')
                # eraseBetween from first char up to and including first "/"
                slash_idx = ns_2.find('/')
                if slash_idx != -1:
                    ns_3 = ns_2[slash_idx:]
                else:
                    ns_3 = ns_2
                # ns_4 = ns_3(2:end)
                ns_4 = ns_3[1:]
                # newStr = erase(ns_4, "/")
                new_str = ns_4.replace('/', '')
                data_temp.labels[i] = new_str

        # Remove empty labels
        data_temp.labels = [label for label in data_temp.labels if label != '']

    elif file_type == 'IK':
        print('%%%% IK file %%%%')

    elif file_type == 'LO':
        print('%%%% External Load file %%%%')

    ## Write motion file
    class MotionData:
        pass

    q = MotionData()
    q.data = num  # new data are taken from the .xls file
    q.labels = data_temp.labels  # labels are taken from the .mot file to modify
    q.nr = row
    q.nc = data_temp.nc

    write_motionFile(q, mot_new_name)
