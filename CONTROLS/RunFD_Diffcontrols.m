
%% Example with data chnaged programmatically in Matlab
clear;close all;

xlsfile='/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Kicking DATA/EMGs.xlsx'; %chnage it accordingly 

[num,txt,~] = xlsread(xlsfile) ;
[row,col]=size(num);
time=num(:,1);

n_sims=50;
% create a matrix of zeros of the same num of col and rows as the one
% inputted - this is created n_sims times.

base_EMGs=zeros(row,col-1,n_sims); %this is a 3D matrix!

% change magnitude
for j=1:n_sims %running 50 times indeed
    
  dec_factor=j/100;
    
  activation_coeff=[1 1 1 1 1 1 1 1]*dec_factor;  % [rect_fem_r	bifemlh_r	bifemsh_r	vast_int_r	glut_max_r	psoas_r	tib_ant_r	med_gas_r]
  base_EMGs(:,:,j)=num(:,2:end).*activation_coeff;
    
  create_control_file( base_EMGs(:,:,j),'controls_kick.xml',[ 'new_control_' num2str(2) '.xml']) ;
 
end
