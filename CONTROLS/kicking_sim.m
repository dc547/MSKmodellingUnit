%% KICKING SIMULATION

xlsfile='/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Kicking DATA/EMGs.xlsx';
template_control='controls_kick.xml';
%% Load exmaple file
[num,txt,~] = xlsread(xlsfile) ;

act=[0.1 0.2 0.3 0.4];

num_it=length(act);

for i=1:num_it
     
    new_RF=num(:,2)*act(i);
    num(:,2)=new_RF;
    
    name=num2str(act(i));
    filename=['/Users/dc547/Desktop/Work/Teaching/HL40064 - MSK Modelling/2020_21/Projects/Kicking DATA/new_control_' name '.xml'];
    
    
    create_control_file(num,template_control,filename,txt)
    
end


