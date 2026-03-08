import opensim as osim

from mot_creator import mot_creator
from states_creator import states_creator
from prescribeMotionInModel_customCoordinates import prescribeMotionInModel_customCoordinates
from FD_prescribed import FD_prescribed


def prescribe_and_simulate(states_input, states_example_file, states_output_file,
                           mot_input, mot_example_file, new_mot_name, Model_In,
                           results_FD_name):
    """Prescribing motion to model and run simulations.

    Parameters
    ----------
    states_input : str or array-like
        Path where you saved the manually written .sto files for FD INITIAL
        CONDITION or array containing the data.
    states_example_file : str
        Filename of the .sto file that is coming from an OpenSim FD output.
    states_output_file : str
        Filename for the new .sto file created with this function.
    mot_input : str or array-like
        File containing the motion data you want to change (it can be an
        Excel file or an array).
    mot_example_file : str
        Filename of the .mot file that includes the right coordinate names
        (from IK?).
    new_mot_name : str
        Filename for the new .mot file created.
    Model_In : str
        Filename of the Model used in the main path.
    results_FD_name : str
        Name for the FD results.
    """

    ## Creating .mot
    mot_creator(mot_example_file, mot_input, new_mot_name, 'FD')

    ## Creating .sto
    states_creator(states_example_file, states_input, states_output_file)

    ## Prescribing Kinematics into the model
    # NOTE: update this path to match your local environment
    Model_Out = '/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Ella/Prescribed_model.osim'
    prescribeMotionInModel_customCoordinates(Model_In, new_mot_name, Model_Out)

    ## Running FD
    FD_prescribed(states_output_file, new_mot_name, Model_Out, results_FD_name)
