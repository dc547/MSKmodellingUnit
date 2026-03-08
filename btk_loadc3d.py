import numpy as np
import warnings

def btk_loadc3d(file=None, grw_threshold=5):
    """Load data from a C3D file into a structured dictionary.

    Function to load the data from a c3d file into the structured dict data.
    The file may be excluded if you wish to choose it from a dialog box.

    Parameters
    ----------
    file : str, optional
        The file path that you wish to load (leave blank to choose from a
        dialog box).
    grw_threshold : float, optional
        The force threshold for calculating the GRW (default 5 N).

    Returns
    -------
    data : dict
        Dictionary containing the following nested structures:
            marker_data - any calculated data from the reconstructed C3D
                file including marker trajectories and any calculated angles,
                moments, powers or GRF data.
            analog_data - analog data (often sampled at a higher rate) including
                force plate data and EMG data that might be collected.
            fp_data - structure with the force outputs from the force
                plates including the ground reaction wrench (force vector
                calculated in the global axis frame) and relevant
                sampling and forceplate position information.
            sub_info - extra data from the C3D file if it exists, including
                height and weight etc.

    Notes
    -----
    This function requires the installation of the BTK (Biomechanical
    Toolkit) Python wrapper. Please see http://code.google.com/p/b-tk/
    for more information and cite appropriately.

    Originally written by Glen Lichtwark (The University of Queensland)
    Updated: 06/12/2011
    """

    import btk

    warnings.filterwarnings('ignore')

    # if no file is given then prompt for file
    if file is None:
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            file = filedialog.askopenfilename(
                title='C3D data file...',
                filetypes=[('C3D file', '*.c3d')]
            )
            root.destroy()
            if not file:
                print('No motion file loaded')
                return None
        except ImportError:
            raise ValueError('No file provided and tkinter not available for dialog.')

    # if file is c3d then load using the BTK wrapper
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(file)
    reader.Update()
    acq = reader.GetOutput()

    # save filename to structure
    marker_data = {}
    marker_data['Filename'] = file

    # get first and last frame data
    marker_data['First_Frame'] = acq.GetFirstFrame()
    marker_data['Last_Frame'] = acq.GetLastFrame()

    # get marker data
    markers = {}
    markers_info = {'units': {}, 'frequency': acq.GetPointFrequency()}
    unit_set = set()
    for i in range(acq.GetPointNumber()):
        point = acq.GetPoint(i)
        if point.GetType() == btk.btkPoint.Marker:
            label = point.GetLabel()
            markers[label] = point.GetValues()
            unit_set.add(point.GetUnit())
    if unit_set:
        markers_info['units']['ALLMARKERS'] = list(unit_set)[0]
    else:
        markers_info['units']['ALLMARKERS'] = ''

    marker_data['Markers'] = markers

    # convert data to millimeters if in meters - catch if units have been screwed with
    fnames = list(markers.keys())
    m_mm = 0
    if fnames:
        first_marker = markers[fnames[0]]
        if (np.nanmean(np.abs(first_marker[:, 0])) < 2 and
                np.nanmean(np.abs(first_marker[:, 1])) < 2 and
                np.nanmean(np.abs(first_marker[:, 2])) < 2):
            m_mm = 1

    if markers_info['units']['ALLMARKERS'] == 'm' or m_mm == 1:
        for name in fnames:
            marker_data['Markers'][name] = marker_data['Markers'][name] * 1000
        markers_info['units']['ALLMARKERS'] = 'mm'

    # add the marker data information to the structure
    marker_data['Info'] = markers_info
    marker_data['Info']['NumFrames'] = acq.GetPointFrameNumber()
    # add a timeline field
    freq = marker_data['Info']['frequency']
    num_frames = marker_data['Info']['NumFrames']
    marker_data['Time'] = np.arange(1, num_frames + 1) / freq

    data = {}
    data['marker_data'] = marker_data

    # get analog data
    analogs = {}
    analogs_info = {'units': {}, 'frequency': acq.GetAnalogFrequency()}
    for i in range(acq.GetAnalogNumber()):
        analog = acq.GetAnalog(i)
        label = analog.GetLabel()
        analogs[label] = analog.GetValues()
        analogs_info['units'][label] = analog.GetUnit()

    if analogs:
        analog_data = {}
        analog_data['Channels'] = analogs
        analog_data['Info'] = analogs_info
        analog_num_frames = acq.GetAnalogFrameNumber()
        analog_data['Info']['NumFrames'] = analog_num_frames
        a_freq = analog_data['Info']['frequency']
        analog_data['Time'] = np.arange(1, analog_num_frames + 1) / a_freq
        # write to data structure
        data['analog_data'] = analog_data

    # get analog data (duplicate block in original)
    analogs = {}
    analogs_info = {'units': {}, 'frequency': acq.GetAnalogFrequency()}
    for i in range(acq.GetAnalogNumber()):
        analog = acq.GetAnalog(i)
        label = analog.GetLabel()
        analogs[label] = analog.GetValues()
        analogs_info['units'][label] = analog.GetUnit()

    if analogs:
        analog_data = {}
        analog_data['Channels'] = analogs
        analog_data['Info'] = analogs_info
        analog_num_frames = acq.GetAnalogFrameNumber()
        analog_data['Info']['NumFrames'] = analog_num_frames
        a_freq = analog_data['Info']['frequency']
        analog_data['Time'] = np.arange(1, analog_num_frames + 1) / a_freq
        # write to data structure
        data['analog_data'] = analog_data

    # get the forceplate info (corners etc)
    fp_wrench_filter = btk.btkForcePlatformsExtractor()
    fp_wrench_filter.SetInput(acq)
    fp_wrench_filter.Update()
    fp_collection = fp_wrench_filter.GetOutput()

    if fp_collection.GetItemNumber() > 0:
        # get the ground reaction data
        grw_filter = btk.btkGroundReactionWrenchFilter()
        grw_filter.SetInput(fp_collection)
        grw_filter.SetThresholdValue(grw_threshold)
        grw_filter.Update()
        grw_collection = grw_filter.GetOutput()

        grw_data = []
        fp_info = []
        fps = []
        for j in range(grw_collection.GetItemNumber()):
            wrench = grw_collection.GetItem(j)
            grw_entry = {
                'P': wrench.GetPosition().GetValues(),
                'F': wrench.GetForce().GetValues(),
                'M': wrench.GetMoment().GetValues()
            }
            grw_data.append(grw_entry)

        for j in range(fp_collection.GetItemNumber()):
            fp = fp_collection.GetItem(j)
            fp_entry = {
                'corners': fp.GetCorners(),
                'origin': fp.GetOrigin(),
                'channels': {},
                'type': fp.GetType()
            }
            for ch in range(fp.GetChannelNumber()):
                channel = fp.GetChannel(ch)
                fp_entry['channels'][channel.GetLabel()] = channel.GetValues()
            fps.append(fp_entry)

            fp_info_entry = {
                'frequency': acq.GetAnalogFrequency(),
                'units': {},
                'cal_matrix': fp.GetCalMatrix()
            }
            fp_info.append(fp_info_entry)

        fp_data = {}
        fp_data['GRF_data'] = grw_data
        fp_data['Info'] = fp_info
        fp_data['FP_data'] = fps
        fp_freq = fp_info[0]['frequency']
        n_analog = len(grw_data[0]['P'])
        fp_data['Time'] = np.arange(1, n_analog + 1) / fp_freq
        # write to data structure
        data['fp_data'] = fp_data

    # get scalar data (e.g. ultrasound data is stored as scalar)
    scalars = {}
    scalars_info = {'frequency': acq.GetPointFrequency()}
    for i in range(acq.GetPointNumber()):
        point = acq.GetPoint(i)
        if point.GetType() == btk.btkPoint.Scalar:
            label = point.GetLabel()
            scalars[label] = point.GetValues()

    if scalars:
        scalar_data = {}
        scalar_data['Data'] = scalars
        scalar_data['Info'] = scalars_info
        scalar_data['Time'] = np.arange(1, num_frames + 1) / freq
        data['scalar_data'] = scalar_data

    # get some subject information
    md = acq.GetMetaData()
    sub_info = {}
    sub_info['Filename'] = file

    if md.HasChild('SUBJECTS'):
        subjects = md.FindChild('SUBJECTS').value()
        if subjects.HasChild('NAMES'):
            names_info = subjects.FindChild('NAMES').value().GetInfo()
            if names_info.GetDimensionNumber() > 0:
                sub_info['Name'] = names_info.ToString()[0].strip() if names_info.ToString() else 'UNKNOWN'
            else:
                sub_info['Name'] = 'UNKNOWN'
        else:
            sub_info['Name'] = 'UNKNOWN'
        if subjects.HasChild('MARKER_SETS'):
            ms_info = subjects.FindChild('MARKER_SETS').value().GetInfo()
            sub_info['MarkerSet'] = ms_info.ToString()[0].strip() if ms_info.ToString() else 'UNKNOWN'
        else:
            sub_info['MarkerSet'] = 'UNKNOWN'
    else:
        sub_info['Name'] = 'UNKNOWN'
        sub_info['MarkerSet'] = 'UNKNOWN'

    if md.HasChild('PROCESSING'):
        processing = md.FindChild('PROCESSING').value()
        sub_info['Processing_Data'] = {}
        for i in range(processing.GetChildNumber()):
            child = processing.GetChild(i)
            label = child.GetLabel()
            info = child.GetInfo()
            if info.GetFormatAsString() == 'Real':
                sub_info['Processing_Data'][label] = info.ToDouble()
            else:
                sub_info['Processing_Data'][label] = info.ToString()

        if 'Bodymass' in sub_info['Processing_Data']:
            data['Mass'] = sub_info['Processing_Data']['Bodymass']
        if 'Height' in sub_info['Processing_Data']:
            data['Height'] = sub_info['Processing_Data']['Height']

    data['Name'] = sub_info['Name']
    data['sub_info'] = sub_info

    return data
