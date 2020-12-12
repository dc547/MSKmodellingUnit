
function create_control_file(xlsfile,template_control,filename,label)
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
% OpenSim using the control editor on the GUI. It is control_kick.xml in
% the example.
%
% (3) filename - (string) - Filename for the new control file created
%
% (4) label - (array of strings) - Array with labels for controls (this is
% needed if you are inputting activations via Matlab
%% Originally written by D. Cazzola, Uni of Bath, 10/11/2020
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Cheking inputs
if nargin ==4
    if exist('label','var') ~= 1 && ischar(xlsfile)
        warning('Check you are inputting controls via Excel file');
    elseif exist('label','var') ~= 1 && ~ischar(xlsfile)
        warning('LABEL input missing - States NOT CREATED');
        return;
    end
end


%% Load xml file as template
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
if ischar(xlsfile)
    [num,txt,~] = xlsread(xlsfile) ;
    [row,col]=size(num);
else % when input file is a Matlab matrix or array
    num=xlsfile;
    time=num(:,1);
    row=size(num,1);
    col=size(num,2);
    txt=label;
    
end

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