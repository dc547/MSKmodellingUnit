"""Create control file from Excel or numpy array.

EXAMPLE
    create_control_file('EMG_template.xls', 'controls_kick.xml',
                        'new_control.xml')

Parameters
----------
xlsfile : str or numpy.ndarray
    Filename of the Excel file containing new inputs for the controls,
    or a numpy array with the control data (first column is time).
template_control : str
    Template control file (XML) created with OpenSim using the
    control editor on the GUI.
filename : str
    Filename for the new control file created.
label : list of str, optional
    List with labels for controls (needed if inputting activations
    via a numpy array).

Originally written by D. Cazzola, Uni of Bath, 10/11/2020
Python version
"""

import copy
import warnings

import numpy as np
import pandas as pd

from CONTROLS.xml2struct import xml2struct
from CONTROLS.struct2xml import struct2xml


def create_control_file(xlsfile, template_control, filename, label=None):
    """Create an OpenSim control file from Excel data or a numpy array.

    Parameters
    ----------
    xlsfile : str or numpy.ndarray
        Path to an Excel file, or a numpy array of control values.
    template_control : str
        Path to the template XML control file.
    filename : str
        Output path for the new control XML file.
    label : list of str, optional
        Column labels for the controls. Required when xlsfile is a
        numpy array.
    """
    # Checking inputs
    if label is not None:
        if isinstance(xlsfile, str):
            warnings.warn('Check you are inputting controls via Excel file')
    elif not isinstance(xlsfile, str):
        warnings.warn('LABEL input missing - States NOT CREATED')
        return

    # Load xml file as template
    xml = xml2struct(template_control)

    # Work on the template file
    root_key = 'OpenSimDocument'
    controls = xml[root_key]['ControlSet']['objects']

    # Ensure ControlLinear is a list
    cl = controls['ControlLinear']
    if not isinstance(cl, list):
        cl = [cl]
    controls['ControlLinear'] = cl

    # Use the first ControlLinear entry as template
    temp = copy.deepcopy(cl[0])

    # Load xls file or use array
    if isinstance(xlsfile, str):
        df = pd.read_excel(xlsfile)
        txt = list(df.columns)
        num = df.values
        row, col = num.shape
    else:
        num = np.asarray(xlsfile)
        if num.ndim == 1:
            num = num.reshape(-1, 1)
        row, col = num.shape
        # When data is a matrix without the time column, add 1 for the
        # offset used below (label includes time header)
        txt = label if label is not None else [f'col_{i}' for i in range(col)]
        col = len(txt)

    # Remove all ControlLinearNode entries but the first one
    nodes = temp['x_nodes']
    cln = nodes['ControlLinearNode']
    if not isinstance(cln, list):
        cln = [cln]
    node_template = copy.deepcopy(cln[0])
    nodes['ControlLinearNode'] = [node_template]
    temp['x_nodes'] = nodes

    # Update t and values
    new_controls = []
    for i in range(1, col):
        ctrl = copy.deepcopy(temp)
        ctrl.setdefault('Attributes', {})['name'] = str(txt[i])

        node_list = []
        # Start from row index 1, matching the MATLAB original (j=2:row)
        for j in range(1, row):
            node = copy.deepcopy(node_template)
            node['t'] = {'Text': str(num[j, 0])}
            node['value'] = {'Text': str(num[j, i])}
            node_list.append(node)

        ctrl['x_nodes']['ControlLinearNode'] = node_list
        new_controls.append(ctrl)

    controls['ControlLinear'] = new_controls

    # Create xml
    struct2xml(xml, filename)


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 4:
        create_control_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python create_control_file.py <xlsfile> <template_control> <filename>")
