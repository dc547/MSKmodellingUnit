import numpy as np
from scipy.interpolate import interp1d


def trc_refiner_v01(fname, data_dyn, markers):
    """Reorder the lab coordinate system and write an OpenSim TRC file.

    We need to reorder the lab coordinate system to match that of the OpenSim
    system --> SKIP THIS STEP IF LAB COORDINATE SYSTEM IS SAME AS MODEL SYSTEM

    Parameters
    ----------
    fname : str
        Output filename (without .trc extension).
    data_dyn : dict
        Dictionary with marker names as keys and Nx3 numpy arrays as values.
    markers : list of str
        List of marker names to process.

    Returns
    -------
    data : dict
        Dictionary containing processed marker data and TRC file info.
    """

    nmarkers = len(markers)
    data = {}
    data['Markers'] = {}

    # go through each marker field and re-order from Z X Y to X Y Z
    for i in range(nmarkers):
        data_temp = data_dyn[markers[i]]
        data['Markers'][markers[i]] = np.column_stack([
            data_temp[:, 1] * -1,
            data_temp[:, 2],
            data_temp[:, 0] * -1
        ])

    # define some parameters
    nrows = data_temp.shape[0]
    data['Rate'] = 200
    nframe = np.arange(1, nrows + 1)
    time = nframe / data['Rate'] - 1.0 / data['Rate']
    data['time'] = time
    data['Start_Frame'] = 1
    data['End_Frame'] = nrows
    data['units'] = 'mm'

    ##
    # now we need to make the headers for the column headings for the TRC file
    # which are made up of the marker names and the XYZ for each marker

    # first initialise the header with a column for the Frame # and the Time
    # also initialise the format for the columns of data to be written to file
    dataheader1 = 'Frame#\tTime\t'
    dataheader2 = '\t\t'

    # initialise the matrix that contains the data as a frame number and time row
    data_out = np.vstack([nframe, time])

    # now loop through each maker name and make marker name with 3 tabs for the
    # first line and the X Y Z columns with the marker number on the second
    # line all separated by tab delimiters
    for i in range(nmarkers):
        dataheader1 += markers[i] + '\t\t\t'
        dataheader2 += 'X{}\tY{}\tZ{}\t'.format(i + 1, i + 1, i + 1)

        # add 3 rows of data for the X Y Z coordinates of the current marker
        # first check for NaN's and fill with a linear interpolant
        sf = data['Start_Frame'] - 1  # convert to 0-based index
        ef = data['End_Frame']        # exclusive end for slicing
        marker_slice = data['Markers'][markers[i]][sf:ef, :]
        m = np.where(np.isnan(marker_slice[:, 0]))[0]

        if len(m) > 0:
            print('Warning - {} data missing in parts. Frames {}-{}'.format(
                markers[i], m[0] + 1, m[-1] + 1))
            t = time.copy()
            d = marker_slice.copy()
            # remove NaN rows
            mask = ~np.isnan(d[:, 0])
            t_clean = t[mask]
            d_clean = d[mask]
            # linear interpolation with extrapolation
            for col in range(3):
                interp_func = interp1d(t_clean, d_clean[:, col],
                                       kind='linear', fill_value='extrapolate')
                marker_slice[:, col] = interp_func(time)
            data['Markers'][markers[i]][sf:ef, :] = marker_slice

        data_out = np.vstack([data_out, data['Markers'][markers[i]][sf:ef, :].T])

    dataheader1 += '\n'
    dataheader2 += '\n'

    print('Writing trc file...')

    # Output marker data to an OpenSim TRC file

    newfilename = fname + '.trc'
    data['TRC_Filename'] = newfilename

    # open the file
    with open(newfilename, 'w') as fid_1:
        # first write the header data
        fid_1.write('PathFileType\t4\t(X/Y/Z)\t {}\n'.format(newfilename))
        fid_1.write('DataRate\tCameraRate\tNumFrames\tNumMarkers\t'
                     'Units\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n')
        fid_1.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            data['Rate'], data['Rate'], nrows, nmarkers,
            data['units'], data['Rate'], data['Start_Frame'], data['End_Frame']))
        fid_1.write(dataheader1)
        fid_1.write(dataheader2)

        # then write the output marker data
        for col_idx in range(data_out.shape[1]):
            col = data_out[:, col_idx]
            # Frame number (int) and time (float)
            line = '{:d}\t{:.4f}\t'.format(int(col[0]), col[1])
            # Marker coordinate values
            line += '\t'.join(['{:f}'.format(v) for v in col[2:]])
            line += '\n'
            fid_1.write(line)

    # close the file (handled by with statement)

    print('Done.')

    return data
