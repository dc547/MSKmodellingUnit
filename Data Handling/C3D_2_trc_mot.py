import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from btk_loadc3d import btk_loadc3d
from btk_sortc3d import btk_sortc3d


def C3D_2_trc_mot(file=None, marker_names=None):
    """Create .trc and .mot files from .C3D.

    Parameters
    ----------
    file : str, optional
        C3D file to process.
    marker_names : list of str, optional
        List of marker names to extract.

    Returns
    -------
    data : dict
        Dictionary containing marker data, analog data, and force plate data.

    Notes
    -----
    Originally written by Dario Cazzola.

    Example marker_names:
        marker_names = ['RASI', 'LASI', 'STRN', 'CLAV', 'C7', 'T10',
                        'LPEL', 'RPEL', 'RTHI', 'RTHIA', 'RKNE', 'RTIBA',
                        'RTIB', 'RANK', 'RHEE', 'RTOE', 'LANK', 'LTOE',
                        'LTIB', 'LTIBA', 'LKNE', 'LTHI', 'LTHIA', 'RPSI',
                        'LPSI', 'LHEE']
    """

    ## Check input
    if file is None and marker_names is None:
        print('Markers name array and C3D file are missing!')
        return None
    elif file is None:
        print('C3D file is missing!')
        return None
    elif marker_names is None:
        print('Markers name array is missing!')
        return None

    if os.path.dirname(file) == '':
        pname = os.getcwd() + os.sep
        fname = file
    else:
        pname = os.path.dirname(file) + os.sep
        fname = os.path.basename(file)

    os.chdir(pname)

    ## Load the c3d file

    # load the c3d file using BTK
    data = btk_loadc3d(os.path.join(pname, fname), 5)

    ## BTK uses First/Last so convert to fit existing routine so Start/End
    data['marker_data']['Last_Frame'] = (
        data['marker_data']['Last_Frame'] - data['marker_data']['First_Frame']
    )
    data['marker_data']['First_Frame'] = 1

    data['Start_Frame'] = data['marker_data']['First_Frame']
    data['End_Frame'] = data['marker_data']['Last_Frame']

    data['marker_data'] = btk_sortc3d(data['marker_data'], marker_names)  # creates .trc file

    ## C3D TO TRC and MOT
    # NOTE: btk_c3d2trc_v5 is not yet ported to Python.
    # When available, uncomment the following:
    # from btk_c3d2trc_v5 import btk_c3d2trc_v5
    # data = btk_c3d2trc_v5(data, 'off')

    return data
