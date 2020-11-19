
function create_control_file(xlsfile,template_control,filename)
%% Create control file from Excel % 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EXAMPLE
% Call the function as bellow:
% 
% >> create_control_file('EMG_template.xls','controls_kick.xml',
% 'new_control.xml')
%
% (1) xlsfile - (string) - This is the filename of the excel file you 
% have created containing the new inputs for the controls
% 
% (2) template control - (xml) - Template control file created with 
% OpenSim using the control editor on the GUI.
% 
% (3) filename - (string) - Filename for the new control file created
%
%% Originally written by D. Cazzola, Uni of Bath, 10/11/2020
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Load xml file as template
sampleXMLfile = template_control;

xml=xml2struct(sampleXMLfile);

%% Work on the template file

% generate a temp field to get a template for each control point in time
temp=xml.OpenSimDocument.ControlSet.objects.ControlLinear{1};
xml.OpenSimDocument.ControlSet.objects.ControlLinearTemp{1}=temp;

xml.OpenSimDocument.ControlSet.objects = rmfield(xml.OpenSimDocument.ControlSet.objects,'ControlLinear');
xml.OpenSimDocument.ControlSet.objects.ControlLinear=xml.OpenSimDocument.ControlSet.objects.ControlLinearTemp;
xml.OpenSimDocument.ControlSet.objects = rmfield(xml.OpenSimDocument.ControlSet.objects,'ControlLinearTemp');

% Load xls file - first row header and then a matrix containing the data -
% First column is time.
[num,txt,~] = xlsread(xlsfile) ;
[row,col]=size(num);

%remove all Control Linear nodes but the first one using a 'temp' field 
temp2=xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes.ControlLinearNode{1,1};
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes.ControlLinearNodeTemp{1,1}=temp2;

xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes = ... 
    rmfield(xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes,'ControlLinearNode');
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes.ControlLinearNode=...
    xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes.ControlLinearNodeTemp;
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes = ...
    rmfield(xml.OpenSimDocument.ControlSet.objects.ControlLinear{1, 1}.xu_nodes,'ControlLinearNodeTemp');

%% Update t and values
for i=2:col
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1,i-1}.Attributes.name=char(txt{i});

    for j=2:row
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1,i-1}.xu_nodes.ControlLinearNode{1, j-1}.t.Text=num2str(num(j,1));
xml.OpenSimDocument.ControlSet.objects.ControlLinear{1,i-1}.xu_nodes.ControlLinearNode{1, j-1}.value.Text=num2str(num(j,i));
    end
end

%% create xml
struct2xml(xml,filename);

end