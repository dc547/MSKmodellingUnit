%% Run FD with prescribed motion
function FD_prescribed(states_file, mot_file, osimModel_file, results_FD_name)

%% Import the OpenSim modeling classes
import org.opensim.modeling.*

%% LOAD states

kin = read_motionFile(mot_file);
%% Read osim model
osimModel = Model(osimModel_file);
% % states_output_file='/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Ella/states_output_file.sto';
% % 
% % res=Storage(states_output_file);
ft=ForwardTool();
% 
% man=ft.getManager();
% % man.setStateStorage(res);
% % man.setPerformAnalyses(1);
% % man.setWriteToStorage(1);


ft.setModel(osimModel);
ft.setSolveForEquilibrium(0);
ft.setErrorTolerance(0.00000001);
ft.setMaxDT(kin.data(2,1)/10);
ft.setMinDT(kin.data(2,1)/10000);
ft.setInitialTime(0);
ft.setFinalTime(kin.data(end,1));
ft.setName(results_FD_name);%names to be changed depending on input values
ft.setStatesFileName(states_file);
ft.setPrintResultFiles(1);
ft.run();


end