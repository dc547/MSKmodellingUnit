import numpy as np


def read_motionFile(fname):
    """
    Purpose:  This function reads a file in the format of a SIMM motion file
              and returns a data structure.

    Input:    fname is the name of the ascii datafile to be read
              (string)

    Output:   q returns an object with the following attributes:
                q.labels  = list of column labels
                q.data    = numpy array of data
                q.nr      = number of matrix rows
                q.nc      = number of matrix columns

    ASA 12/03
    Modified by Eran Guendelman 09/06
    """

    class MotionData:
        pass

    # Open ascii data file for reading.
    try:
        fid = open(fname, 'r')
    except OSError:
        raise OSError('unable to open ' + fname)

    # Process the file header;
    # store # data rows, # data columns.
    q = MotionData()
    q.nr = 0  # Added to ensure that the q structures from reading a motion file
    q.nc = 0  # are always the same, even if nr and nc are different orders in file.

    nextline = fid.readline().strip('\n')
    while not nextline.lower().startswith('endheader'):
        if nextline.lower().startswith('datacolumns'):
            q.nc = int(nextline[nextline.index(' ') + 1:])
        elif nextline.lower().startswith('datarows'):
            q.nr = int(nextline[nextline.index(' ') + 1:])
        elif nextline.lower().startswith('ncolumns'):
            q.nc = int(nextline[nextline.index('=') + 1:])
        elif nextline.lower().startswith('nrows'):
            q.nr = int(nextline[nextline.index('=') + 1:])
        nextline = fid.readline().strip('\n')

    # Process the column labels.
    nextline = fid.readline().strip('\n')
    if nextline.strip() == '':  # Blank line, so the next one must be the one containing the column labels
        nextline = fid.readline().strip('\n')

    q.labels = nextline.split()[:q.nc]

    # Process the data.
    q.data = np.loadtxt(fid, dtype=float)
    q.data = q.data.reshape((q.nr, q.nc))

    fid.close()

    return q
