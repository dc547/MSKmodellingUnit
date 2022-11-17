function data = C3D_2_trc_mot(file, marker_names)

% This function will create .trc and .mot files from .C3D
% Input - file - c3d file to process
% Originally written by Dario Cazzola

%  EXAMPLE markers_name:
% marker_names = {'RASI', 'LASI', 'STRN', 'CLAV', 'C7', 'T10', 'LPEL', 'RPEL', 'RTHI', ...
% 'RTHIA', 'RKNE', 'RTIBA', 'RTIB', 'RANK', 'RHEE', 'RTOE', 'LANK', 'LTOE', 'LTIB', 'LTIBA', ...
% 'LKNE', 'LTHI', 'LTHIA', 'RPSI','LPSI','LHEE'};...

% % % marker_names = {'L4','Mid Psis','ASIS right','ASIS left', ...
% % %     'Trochanter right' ,'Thigh lateral right', 'Condylus lateralis right', ...
% % %     'Condylus medialis right', 'Shank right', 'Outer ankle-bone right', ...
% % %     'Inner ankle-bone right', 'Forefoot right' ,'Heel right' ,'Foot tip right', ... 
% % %     'Trochanter left', 'Thigh lateral left' ,'Condylus lateralis left', ...
% % %     'Condylus medialis left' ,'Shank left', 'Outer ankle-bone left' ,'Inner ankle-bone left' ,'Forefoot left', ...
% % %     'Heel left'	,'Foot tip left','Vertebra Th8' ,'Lower breast-bone' ,'Upper breast-bone' ,'Vertebra C7', 'Shoulder right', ...
% % %     'Shoulder left'	,'Triceps right','Biceps right','Elbow lateral right', ... 
% % %     'Elbow medial right', 'Wrist lateral right','Wrist medial right', 'Hand right' ,'Triceps left', ... 
% % %     'Biceps left' ,'Elbow lateral left', 'Elbow medial left','Wrist lateral left' ,'Wrist medial left' ,'Hand left', ... 
% % %     'Head temple left', 'Head temple right','Back head left' ,'Back head right'};

% % marker_names = {'RAC' 'LAC' 'RASIS' 'LASIS' 'RPSIS' 'LPSIS'  ...
% % 'RTH1-4' 'LTH1-4' 'RLFC' 'LLFC'...
% % 'RSK1-4' 'LSK1-4' 'RLMAL' 'LLMAL' 'RHEL' 'LHEL' 'RMP5' 'LMT5' 'RMT1' 'LMT1' 'RHAL' 'LHAL'};
% % 

%% Check input
if nargin < 2
    
    switch nargin
        case 0
            disp('Markers name array and C3D file are missing!')
        case 1
            exist marker_names
            if ans == 0
                disp('Markers name array is missing!');
                return
            else
                disp('C3D file is missing!');
            end
    end
else
    
    if isempty(fileparts(file))
        pname = cd;
        pname = [pname '/'];
        fname = file;
    else
        [pname, name, ext] = fileparts(file);
        fname = [name ext];
    end
end

cd(pname);

%% Load the c3dfile

% load the c3d file using BTK
data = btk_loadc3d([pname, fname], 5);

%% BTK uses First/Last so convert to fit existing routine so Start/End
data.marker_data.Last_Frame = data.marker_data.Last_Frame - data.marker_data.First_Frame;
data.marker_data.First_Frame = 1;

data.Start_Frame = data.marker_data.First_Frame;
data.End_Frame = data.marker_data.Last_Frame;


data.marker_data = btk_sortc3d(data.marker_data,marker_names); % creates .trc file


%% C3D TO TRC and MOT
%'v5' of this script is modified from previous ones since person is now
%walking in the 'forward' direction of the treadmill (towards the wall) and
%so coordinate system transformations have changed.

data = btk_c3d2trc_v5(data,'off');




