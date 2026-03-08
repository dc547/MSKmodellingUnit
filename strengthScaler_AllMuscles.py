import opensim as osim
import os


def strengthScaler_AllMuscles(modelPath, muscles_num, n, resultsFolder='Results', addName=''):
    """Scale the max isometric force of all muscles in an OpenSim model.

    Parameters
    ----------
    modelPath : str
        Full path to the OpenSim model file.
    muscles_num : int
        Number of muscles in the model. Obtain via
        OSmodel.getMuscles().getSize().
    n : float
        Scaling percentage (e.g. 100 = no change, 50 = half strength).
    resultsFolder : str, optional
        Folder where the scaled model will be saved. Default is 'Results'.
    addName : str, optional
        Additional name tag for the output model file.

    Returns
    -------
    modelOutputPath : str
        Full path to the printed scaled model.
    """

    # create instance of the model
    myModel = osim.Model(modelPath)
    myModel.initSystem()

    # make the scaling factor a decimal (if 100% then 1, if 50% then 0.5)
    scalingFactor = n / 100

    # multiply all muscles in the model by scalingFactor
    for ii in range(muscles_num):
        b = myModel.getMuscles().get(ii).getMaxIsometricForce()
        myModel.getMuscles().get(ii).setMaxIsometricForce(b * scalingFactor)

    # Print the model out to the results file, ready to be used by the
    # cmcTool
    modelOutputPath = os.path.join(resultsFolder,
                                   'myModel_' + addName + '_' + str(round(n)) + '.osim')
    myModel.printToXML(modelOutputPath)

    print('model printed')

    return modelOutputPath
