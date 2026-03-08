# ----------------------------------------------------------------------- #
# The OpenSim API is a toolkit for musculoskeletal modeling and           #
# simulation. See http://opensim.stanford.edu and the NOTICE file         #
# for more information. OpenSim is developed at Stanford University       #
# and supported by the US National Institutes of Health (U54 GM072970,    #
# R24 HD065690) and by DARPA through the Warrior Web program.             #
#                                                                         #
# Copyright (c) 2005-2017 Stanford University and the Authors             #
# Author(s): Dominic Farris                                               #
#                                                                         #
# Licensed under the Apache License, Version 2.0 (the "License");         #
# you may not use this file except in compliance with the License.        #
# You may obtain a copy of the License at                                 #
# http://www.apache.org/licenses/LICENSE-2.0.                             #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or         #
# implied. See the License for the specific language governing            #
# permissions and limitations under the License.                          #
# ----------------------------------------------------------------------- #

# prescribeMotionInModel_customCoordinates.py
# Author: Dominic Farris

import math
import opensim as osim


def prescribeMotionInModel_customCoordinates(Model_In=None, Mot_In=None,
                                             Model_Out=None,
                                             not_prescr_coords=None):
    """
    Function to take an existing model file and coordinate data accessed
    from an IK solution and write it as a Natural Cubic Spline Function
    to the Prescribed Function method of a Coordinate to a model file.
    Based off work done by Dominic Farris.

    Input:  Model_In - Existing model stored in osim file (string path)
            Mot_In - A file containing motion data for the particular
                     model (string path)
            Model_Out - The output file with prescribed motion (string path)
            not_prescr_coords - list of coordinate names not to be
                prescribed (they need to be in order of appearance
                in the model)

    e.g. prescribeMotionInModel_customCoordinates(
             'myInputModel.osim', 'myMotionFile.mot',
             'myOutputModel.osim', ['coord1', 'coord2'])

    Originally written by Dominic Farris (North Carolina State University).
    Please acknowledge contribution in published academic works.
    Last updated - 17/07/2012
    """

    # If there aren't enough arguments passed in, the system will ask
    # the user to manually select file(s).
    # Note: tkinter.filedialog.askopenfilename could be used for
    # interactive file selection, but here we require arguments directly.

    if not_prescr_coords is None:
        not_prescr_coords = []

    if Model_In is None:
        raise ValueError('Model_In is required. Please provide a path to '
                         'an .osim model file.')
    if Mot_In is None:
        raise ValueError('Mot_In is required. Please provide a path to '
                         'a .mot motion file.')

    if Model_Out is None:
        fileoutpath = Model_In[:-5] + '_Prescribed.osim'
    else:
        fileoutpath = Model_Out

    modelfilepath = Model_In
    motfilepath = Mot_In

    # Initialize model
    osimModel = osim.Model(modelfilepath)

    # Create the coordinate storage object from the input .sto file
    coordinateSto = osim.Storage(motfilepath)

    # Rename the modified Model
    osimModel.setName('modelWithPrescribedMotion')

    # get coordinate set from model, and count the number of coordinates
    modelCoordSet = osimModel.getCoordinateSet()
    nCoords = modelCoordSet.getSize()

    nt_coord = 0  # index into not_prescr_coords list (0-based)

    # for all coordinates in the model, create a function and prescribe
    for i in range(nCoords):

        # construct ArrayDouble objects for time and coordinate values
        Time = osim.ArrayDouble()
        coordvalue = osim.ArrayDouble()

        # Get the coordinate set from the model
        currentcoord = modelCoordSet.get(i)

        # Get the Time stamps and Coordinate values
        coordinateSto.getTimeColumn(Time)
        coordinateSto.getDataColumn(currentcoord.getName(), coordvalue)

        # Check if it is a rotational or translational coordinate
        motion = currentcoord.getMotionType()

        # construct a SimmSpline object (previously NaturalCubicSpline)
        Spline = osim.SimmSpline()

        ## DO NOT PRESCRIBE FOR SPECIFIC COORDINATES
        if nt_coord >= len(not_prescr_coords):
            nt_coord = 0

        if (len(not_prescr_coords) > 0
                and currentcoord.getName() == not_prescr_coords[nt_coord]):
            print('Locked Coord')
        else:
            # Now to write Time and coordvalue to Spline
            if motion == osim.Coordinate.MotionType.Rotational:
                # if the motion type is rotational we must convert to
                # radians from degrees
                for j in range(coordvalue.getSize()):
                    Spline.addPoint(Time.getitem(j),
                                    coordvalue.getitem(j) / (180.0 / math.pi))
            else:
                # else we assume it's translational and can be left 'as is'
                for j in range(coordvalue.getSize()):
                    Spline.addPoint(Time.getitem(j), coordvalue.getitem(j))

            # Add the SimmSpline to the PrescribedFunction of the
            # Coordinate being edited
            currentcoord.setPrescribedFunction(Spline)
            currentcoord.setDefaultIsPrescribed(True)

        nt_coord += 1

    # Save the Modified Model to a file
    osimModel.print(fileoutpath)
    print('The new model has been saved at ' + fileoutpath)
