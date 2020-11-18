function mot_creator(mot_example, input_file, mot_new_name,file_type)
%% Modify .mot file from .xls %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EXAMPLE
% This can be used to modify both kinematics and kinetics .mot files
%
%
% (1) mot_example - (string) - This is the filename of the .mot file
% you want to modify.
%
% (2) input_file - (string or matrix) - This is the filename of the excel file
% including the new data or a matlab matrix including data
%
% (3) mot_name - (string) - Filename for the new .mot file created
%
% (4) file_type - (string) - options: (FD) .mot from forward dynamics;
% (IK) .mot from IK; (LO) .mot for creating external load file;
%
%
%% Originally written by D. Cazzola, Uni of Bath, 10/11/2020
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Read motion file
data_temp=read_motionFile(mot_example);

if contains(input_file,'.xls')
    %% Import digitised points from .xls
    [num,~,~] = xlsread(input_file) ;
    [row,~]=size(num);
    
    %Get the time, which should be the first column in the .xls file
    
    time=num(:,1);
    
    if size(num,2)~=size(data_temp.data,2)
        warning('The number of states or external load is incorrect. Check both mot_exmaple and the input file.')
        return
    end
else %expecting a matrix with time as first column and then data
    
    num=input_file;
    time=num(:,1);
end

%% CASES

switch file_type
    case 'FD'
        disp('%%%% FD file %%%%');
        Index1 = find(contains(data_temp.labels,'speed'));
        data_temp.labels(Index1)=[];
        data_temp.data(:,Index1)=[];
        Index2 = find(contains(data_temp.labels,'forceset'));
        data_temp.labels(Index2)=[];
        data_temp.data(:,Index2)=[];
    case 'IK'
        disp('%%%% IK file %%%%');
    case 'LO'
        disp('%%%% External Load file %%%%');
end
%% Write motion file
q.data=num; % new data are taken from the .xls file
q.labels=data_temp.labels; %labels are taken from the .mot file to modify
q.nr=row;
q.nc=data_temp.nc;

write_motionFile(q, mot_new_name);
end
