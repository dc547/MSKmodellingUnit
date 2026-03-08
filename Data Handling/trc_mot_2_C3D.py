"""Create new C3D files from .trc and .mot files.

Uses the ezc3d Python library for reading/writing C3D files.

Notes
-----
Originally written in MATLAB by Dario Cazzola.
"""

import os
import sys
import numpy as np
import ezc3d

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from read_motionFile import read_motionFile


def read_trcFile(trc_path):
    """Read an OpenSim TRC file and return a data structure.

    Parameters
    ----------
    trc_path : str
        Path to the .trc file.

    Returns
    -------
    trc_data : object
        Object with attributes:
            labels : list of str - column labels
            data   : numpy array - numeric data
    """

    class TRCData:
        pass

    trc_data = TRCData()

    with open(trc_path, 'r') as f:
        # Line 1: header info (PathFileType ...)
        f.readline()
        # Line 2: column description header
        f.readline()
        # Line 3: rate, camera rate, num frames, num markers, units, etc.
        f.readline()
        # Line 4: marker names header
        header_line = f.readline().strip()
        trc_data.labels = header_line.split('\t')
        # Line 5: X/Y/Z sub-headers
        f.readline()

        # Read the numeric data
        data_lines = []
        for line in f:
            line = line.strip()
            if line:
                vals = []
                for v in line.split('\t'):
                    v = v.strip()
                    if v == '':
                        vals.append(np.nan)
                    else:
                        vals.append(float(v))
                data_lines.append(vals)

    trc_data.data = np.array(data_lines)
    return trc_data


if __name__ == '__main__':

    ## Load .trc files
    trc_path = 'Run_200 02.trc'
    trc_data = read_trcFile(trc_path)
    Markers_labels = trc_data.labels
    Markers_data = trc_data.data
    sf_k = 1.0 / (Markers_data[1, 1] - Markers_data[0, 1])

    ## Load .mot files
    mot_path = 'Run_200 02_newCOP3.mot'
    mot_data = read_motionFile(mot_path)
    GRFs_labels = mot_data.labels
    GRFs_data = mot_data.data
    sf_grf = 1.0 / (GRFs_data[1, 0] - GRFs_data[0, 0])

    ## Prep data for ezc3d format
    # Remove frames and time
    Markers_data = Markers_data[:-1, 2:]

    firstFrame_k = int(Markers_data[0, 0])
    lastFrame_k = int(Markers_data[-1, 0])
    # Take every 3rd label starting from index 2 (matching MATLAB 3:3:end)
    Markers_labels = [Markers_labels[i] for i in range(2, len(Markers_labels), 3)]

    GRFs_data = GRFs_data[:-1, 1:]
    firstFrame_g = int(GRFs_data[0, 0] * sf_grf)
    lastFrame_g = int(GRFs_data[-1, 0] * sf_grf)
    GRFs_labels = GRFs_labels[1:]
    n_labels_grf = len(GRFs_labels)

    # Transpose to get the XYZ in rows
    Markers_data_T = Markers_data.T

    # Creating 3D matrix
    n_markers = Markers_data_T.shape[0]
    n_frames = Markers_data_T.shape[1]

    n_point_markers = n_markers // 3
    # Reshape into (3, n_point_markers, n_frames) for ezc3d
    Markers_data_ezc3d = np.zeros((4, n_point_markers, n_frames))
    for i in range(n_frames):
        for k in range(n_point_markers):
            j = k * 3
            Markers_data_ezc3d[0:3, k, i] = Markers_data_T[j:j + 3, i]
        Markers_data_ezc3d[3, :, i] = 1.0  # residuals row

    ## Create C3D

    # Load an empty c3d structure
    c3d = ezc3d.c3d()

    # Add kinematics frame rate
    c3d['parameters']['POINT']['RATE']['value'] = [int(sf_k)]

    # Add Markers label
    c3d['parameters']['POINT']['LABELS']['value'] = Markers_labels

    # Add 3d data points
    c3d['data']['points'] = Markers_data_ezc3d

    c3d['header']['points']['size'] = n_point_markers
    c3d['header']['points']['frame_rate'] = sf_k
    c3d['header']['points']['first_frame'] = firstFrame_k
    c3d['header']['points']['last_frame'] = lastFrame_k

    # Add GRFs frame rate
    c3d['parameters']['ANALOG']['RATE']['value'] = [int(sf_grf)]
    # GRFs labels
    c3d['parameters']['ANALOG']['LABELS']['value'] = GRFs_labels
    # GRFs data - ezc3d expects shape (n_subframes, n_channels, n_frames)
    analog_ratio = int(sf_grf / sf_k)
    n_analog_channels = GRFs_data.shape[1]
    n_analog_frames = GRFs_data.shape[0]
    n_point_frames = n_analog_frames // analog_ratio
    GRFs_data_ezc3d = np.zeros((1, n_analog_channels, n_analog_frames))
    GRFs_data_ezc3d[0, :, :] = GRFs_data.T
    c3d['data']['analogs'] = GRFs_data_ezc3d

    c3d['header']['analogs']['size'] = n_labels_grf
    c3d['header']['analogs']['frame_rate'] = sf_grf
    c3d['header']['analogs']['first_frame'] = firstFrame_g
    c3d['header']['analogs']['last_frame'] = lastFrame_g

    ## Write a new modified C3D and read back the data
    c3d.write('temporary.c3d')

    c3d_to_compare = ezc3d.c3d('temporary.c3d')

    # Print the header
    print('%% ---- HEADER ---- %%')
    print('Number of points = {}'.format(
        c3d_to_compare['header']['points']['size']))
    print('Point frame rate = {:.1f}'.format(
        c3d_to_compare['header']['points']['frame_rate']))
    print('Index of the first point frame = {}'.format(
        c3d_to_compare['header']['points']['first_frame']))
    print('Index of the last point frame = {}'.format(
        c3d_to_compare['header']['points']['last_frame']))
    print()
    print('Number of analogs = {}'.format(
        c3d_to_compare['header']['analogs']['size']))
    print('Analog frame rate = {:.1f}'.format(
        c3d_to_compare['header']['analogs']['frame_rate']))
    print('Index of the first analog frame = {}'.format(
        c3d_to_compare['header']['analogs']['first_frame']))
    print('Index of the last analog frame = {}'.format(
        c3d_to_compare['header']['analogs']['last_frame']))
    print()
    print()
