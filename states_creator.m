function states_creator(states_example_file, states_file, states_output_file)
%% Load states file created via FD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INPUTS

% (1) states_example_file - (string) - This is the filename of the .sto
% file that is coming from an OpenSim FD output
%
% (2) states_file_excel - (string) - Filename of the .xls file you have
% manually changed in Excel
%
% (3) states_output_file - (string) - Filename for the new .sto file
% created with this function
%
%% Originally written by D. Cazzola, Uni of Bath, 10/11/2020
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Load excel file
if contains(input_file,'.xls')
[num,~,~] = xlsread(states_file) ;
[row,~]=size(num);
else
    num=states_file;
    time=num(:,1);
end
%% Load states example
sto=read_motionFile(states_example_file);

%% check compatibility
if size(num,2)~=size(sto.data,2)
    warning('The number of states is incorrect. Check both sto_exmaple and the input file.')
    return
end

% just get the first line for the initial conditions
if row==1
    data=num; %check that the time is in line with other file inputted in the FD
    displ('States to be used as initial conditions for FD');
else
    data=num(1,:);
    warning('States present for more than one frame - Correct?');
end

%% write states

sto.data(1,2:end)=data(1,2:end); %time starts at 0 now
sto.data(2:end,:)=[];
write_motionFile(sto, states_output_file);
end