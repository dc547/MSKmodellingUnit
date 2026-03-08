import numpy as np
import copy


def btk_sortc3d(marker_data, marker_names=None, calc_markers=None):
    """Sort data loaded from a C3D file so that data is appropriately labelled.

    Function to sort data loaded from C3D file with btk_loadc3d so that
    data is appropriately labelled as a marker, angle, moment etc. This is
    necessary when data is processed using the PiG model, where extra marker
    data representing joint moments, centre etc are made and we want to be
    able to distinguish which is which.

    Parameters
    ----------
    marker_data : dict
        Dictionary containing data from C3D file (generated using
        btk_loadc3d). Must contain a 'Markers' key with marker data.
    marker_names : list of str, optional
        A list of strings containing the marker names that are to be taken
        from the c3d file and placed into a marker structure (all other
        3D targets will be placed in another structure variable called
        Other_Markers) - with exception of anything containing Angle,
        Force, Moment, Power, GRF, Mass which are stored as individual
        structure variables. If not given then all 3D data will be used.
    calc_markers : list of str, optional
        List of any additional markers to be placed somewhere special
        (e.g. calculated markers of joint centres).

    Returns
    -------
    data_out : dict
        New dictionary which has data sorted into new fields depending on
        whether it is Marker data, Angle data, Moment data etc.
        e.g. data['Angles']['LAnkleAngle'] rather than
        data['Markers']['LAnkleAngle']

    Notes
    -----
    Originally written by Glen Lichtwark (The University of Queensland)
    Updated: Sept, 2012
    """

    # work on a copy so we don't mutate the original
    marker_data = copy.deepcopy(marker_data)

    if marker_names is None:
        marker_names = list(marker_data['Markers'].keys())

    if calc_markers is None:
        calc_markers = []

    # load the field names
    names = list(marker_data['Markers'].keys())

    # go through each field name and determine if it is something which can be
    # sorted into a specific field reference
    for name in names:

        a = marker_data['Markers'][name]  # load the data in the field

        # if the field name is in the marker cell array then add it to the Marker structure
        if name in marker_names and isinstance(a, np.ndarray) and a.ndim == 2 and a.shape[1] == 3:
            continue

        if calc_markers:
            # if the field name is in the calc_markers list then add it to Calc_Markers
            if name in calc_markers:
                if 'Calc_Markers' not in marker_data:
                    marker_data['Calc_Markers'] = {}
                marker_data['Calc_Markers'][name] = a
                del marker_data['Markers'][name]
                continue

        if 'Angle' in name:  # find angles
            if 'Angles' not in marker_data:
                marker_data['Angles'] = {}
            marker_data['Angles'][name] = a  # add to the new reference field
            del marker_data['Markers'][name]  # remove the original field
            continue

        if 'Force' in name:  # find forces
            if 'Force' not in marker_data:
                marker_data['Force'] = {}
            marker_data['Force'][name] = a
            del marker_data['Markers'][name]
            continue

        if 'Moment' in name:  # find moments
            if 'Moment' not in marker_data:
                marker_data['Moment'] = {}
            marker_data['Moment'][name] = a
            del marker_data['Markers'][name]
            continue

        if 'Power' in name:  # find powers
            if 'Power' not in marker_data:
                marker_data['Power'] = {}
            marker_data['Power'][name] = a
            del marker_data['Markers'][name]
            continue

        if 'GRF' in name:  # find GRFs
            if 'GRF' not in marker_data:
                marker_data['GRF'] = {}
            marker_data['GRF'][name] = a
            del marker_data['Markers'][name]
            continue

        if 'Mass' in name:  # find centre of mass fields
            if 'COM' not in marker_data:
                marker_data['COM'] = {}
            marker_data['COM'][name] = a
            del marker_data['Markers'][name]
            continue

        if 'Other_Markers' not in marker_data:
            marker_data['Other_Markers'] = {}
        marker_data['Other_Markers'][name] = a
        del marker_data['Markers'][name]

    # output data
    data_out = marker_data
    return data_out
