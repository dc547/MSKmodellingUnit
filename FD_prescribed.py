## Run FD with prescribed motion
import opensim as osim
import numpy as np
from read_motionFile import read_motionFile


def FD_prescribed(states_file, mot_file, osimModel_file, results_FD_name):

    ## Import the OpenSim modeling classes
    # (handled via 'import opensim as osim' at module level)

    ## LOAD states
    kin = read_motionFile(mot_file)

    ## Read osim model
    osimModel = osim.Model(osimModel_file)
    # states_output_file='/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Ella/states_output_file.sto'
    #
    # res=osim.Storage(states_output_file)
    ft = osim.ForwardTool()
    #
    # man=ft.getManager()
    # man.setStateStorage(res)
    # man.setPerformAnalyses(1)
    # man.setWriteToStorage(1)

    ft.setModel(osimModel)
    ft.setSolveForEquilibrium(0)
    ft.setErrorTolerance(0.00000001)
    ft.setMaxDT(kin.data[1, 0] / 10)
    ft.setMinDT(kin.data[1, 0] / 10000)
    ft.setInitialTime(0)
    ft.setFinalTime(kin.data[-1, 0])
    ft.setName(results_FD_name)  # names to be changed depending on input values
    ft.setStatesFileName(states_file)
    ft.setPrintResultFiles(1)
    ft.run()
