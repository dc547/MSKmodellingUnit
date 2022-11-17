%% Create new c3d files from .trc and .mot


%% Load .trc files
trc_path='Run_200 02.trc';
trc_data=read_trcFile(trc_path);
Markers_labels=trc_data.labels;
Markers_data=trc_data.data;
sf_k=1/(Markers_data(2,2)-Markers_data(1,2));

%% Load .mot files
mot_path='Run_200 02_newCOP3.mot';
mot_data=read_motionFile(mot_path);
GRFs_labels=mot_data.labels;
GRFs_data=mot_data.data;
sf_grf=1/(GRFs_data(2,1)-GRFs_data(1,1));

%% Prep data for ezc3d format
% Remove frames and time
Markers_data=Markers_data(1:end-1,3:end);

firstFrame_k=Markers_data(1,1);
lastFrame_k=Markers_data(end,1);
Markers_labels=trc_data.labels(:,3:3:end);


GRFs_data=GRFs_data(1:end-1,2:end);
firstFrame_g=GRFs_data(1,1)*sf_grf;
lastFrame_g=GRFs_data(end,1)*sf_grf;
GRFs_labels=mot_data.labels(:,2:end);
n_labels_grf=length(GRFs_labels);

% Traspose to get the XYZ in rows
Markers_data_T=Markers_data';

% Creating 3D matrix
n_markers=size(Markers_data_T,1);
n_frames=size(Markers_data_T,2);

Markers_data_ezc3d=[];
temp=[];
for i=1:n_frames
    k=1;
    for j=1:3:n_markers
        
        temp(1:3,k)=Markers_data_T(j:j+2,k);
        k=k+1;
    end
    Markers_data_ezc3d = cat(3,Markers_data_ezc3d,temp);
    
end
%% Create C3D

% Load an empty c3d structure
c3d = ezc3dRead();

% Add kinematics frame rate
c3d.parameters.POINT.RATE.DATA = sf_k;

% Add Markers label
c3d.parameters.POINT.LABELS.DATA = Markers_labels;
% Add 3d data points

c3d.data.points=[];
c3d.data.points = Markers_data_ezc3d;

c3d.header.points.size=n_markers/3;
c3d.header.points.frameRate=sf_k;
c3d.header.points.firstFrame=firstFrame_k;
c3d.header.points.lastFrame=lastFrame_k;

% chanfing residuals to make it work
c3d.data.meta_points.residuals=zeros(1,n_markers/3,n_frames);
c3d.data.meta_points.camera_masks=zeros(7,n_markers/3,n_frames);


% Add GRFs frame rate
c3d.parameters.ANALOG.RATE.DATA = sf_grf;
% GRFs labels
c3d.parameters.ANALOG.LABELS.DATA = GRFs_labels;
% GRFs data
c3d.data.analogs = GRFs_data;

c3d.header.analogs.size=n_labels_grf;
c3d.header.analogs.frameRate=sf_grf;
c3d.header.analogs.firstFrame=firstFrame_g;
c3d.header.analogs.lastFrame=lastFrame_g;

%% Write a new modified C3D and read back the data
ezc3dWrite('temporary.c3d', c3d);

c3d_to_compare = ezc3dRead('temporary.c3d');
 
% Print the header
fprintf('%% ---- HEADER ---- %%\n');
fprintf('Number of points = %d\n', c3d_to_compare.header.points.size);
fprintf('Point frame rate = %1.1f\n', c3d_to_compare.header.points.frameRate);
fprintf('Index of the first point frame = %d\n', c3d_to_compare.header.points.firstFrame);
fprintf('Index of the last point frame = %d\n', c3d_to_compare.header.points.lastFrame);
fprintf('\n');
fprintf('Number of analogs = %d\n', c3d_to_compare.header.analogs.size');
fprintf('Analog frame rate = %1.1f\n', c3d_to_compare.header.analogs.frameRate);
fprintf('Index of the first analog frame = %d\n', c3d_to_compare.header.analogs.firstFrame);
fprintf('Index of the last analog frame = %d\n', c3d_to_compare.header.analogs.lastFrame);
fprintf('\n');
fprintf('\n');
