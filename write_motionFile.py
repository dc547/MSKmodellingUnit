import numpy as np


def write_motionFile(q, fname):
    """
    Purpose:  This function writes a SIMM motion file from a data structure.

    Input:    q is an object with the following attributes:
                q.labels  = list of column labels
                q.data    = numpy array of data
              fname is the name of the ascii datafile to be written
              (string)
    """

    # Validate that the number of labels matches the number of data columns.
    if len(q.labels) != q.data.shape[1]:
        raise ValueError("Number of labels doesn't match number of columns")

    # Validate that the first column is 'time'.
    if q.labels[0] != 'time':
        raise ValueError("Expected 'time' as first column")

    # Open file for writing.
    try:
        fid = open(fname, 'w')
    except OSError:
        raise OSError('unable to open ' + fname)

    with fid:
        # Write the file header.
        fid.write('name %s\n' % fname)
        fid.write('datacolumns %d\n' % q.data.shape[1])
        fid.write('datarows %d\n' % q.data.shape[0])
        fid.write('range %f %f\n' % (np.min(q.data[:, 0]), np.max(q.data[:, 0])))
        fid.write('endheader\n')

        # Write the column labels.
        for label in q.labels:
            fid.write('%20s\t' % label)
        fid.write('\n')

        # Write the data.
        for i in range(q.data.shape[0]):
            for j in range(q.data.shape[1]):
                fid.write('%20.8f\t' % q.data[i, j])
            fid.write('\n')
