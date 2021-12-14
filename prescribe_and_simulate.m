function prescribe_and_simulate (states_input,states_example_file,states_output_file,...
    mot_input,mot_example_file, new_mot_name,Model_In,results_FD_name)
%% Prescribing motion to model and run simulations

% (1) states_input - (string or Matlab matrix/array) - Path where you saved the manually written .sto
% files for FD INITIAL CONDITION or Matab matrix/array containing the data

% (2) state_exampel_file - (string) - This is the filename of the .sto  
% file that is coming from an OpenSim FD output

% (3) states_output_file - (string) - Filename for the new .sto file
% created with this function

% (4) mot_input - (string or Matlab matrix/array) - File containing the
% motion data you want to change (it an be an Excel file or a Matlab
% matrix)

% (5) mot_example_file - (string) - This is the filename of the .mot  
% file that includes the right coordinate names (from IK?)

% (6) mot_new_name - (string) - Filename for the new .mot file created

% (7) Model_in - (string) - filename of the Model used in the main path

% (8) results_FD_name - (string) - name for the FD results

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import org.opensim.modeling.*


        %% Creating .mot
        mot_creator(mot_example_file, mot_input, new_mot_name,'FD');              
        
        %% Creating .sto
        states_creator(states_example_file, states_input, states_output_file);
        
        %% Prescribing Kinematics into the model
        Model_Out='/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Ella/Prescribed_model.osim';
        prescribeMotionInModel(Model_In, new_mot_name, ...
            Model_Out)
        
        %% Running FD
        FD_prescribed(states_output_file, new_mot_name, Model_Out, results_FD_name)
   
    
end


