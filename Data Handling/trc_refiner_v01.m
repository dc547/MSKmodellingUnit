function data = trc_refiner_v01(fname,data_dyn,markers)



% we need to reorder the lab coordinate system to match that of the OpenSim
% system --> SKIP THIS STEP IF LAB COORDINATE SYSTEM IS SAME AS MODEL
% SYSTEM

nmarkers=size(markers,2);

% go through each marker field and re-order from Z X Y to X Y Z
for i = 1:nmarkers
   data_temp=data_dyn.(markers{i});
    data.Markers.(markers{i}) =  [data_temp(:,2).*-1 ...
       data_temp(:,3) data_temp(:,1).*-1];
end

% define some parameters 

nrows = size(data_temp,1);
data.Rate=200;
nframe = 1:nrows;
time = (nframe/data.Rate)-1/data.Rate;
data.time = time;
data.Start_Frame=1;
data.End_Frame=nrows;
data.units='mm';

%%
% now we need to make the headers for the column headings for the TRC file
% which are made up of the marker names and the XYZ for each marker

% first initialise the header with a column for the Frame # and the Time
% also initialise the format for the columns of data to be written to file
dataheader1 = 'Frame#\tTime\t';
dataheader2 = '\t\t';
format_text = '%i\t%2.4f\t';
% initialise the matrix that contains the data as a frame number and time row
data_out = [nframe; time];

% now loop through each maker name and make marker name with 3 tabs for the
% first line and the X Y Z columns with the marker numnber on the second
% line all separated by tab delimeters
% each of the data columns (3 per marker) will be in floating format with a
% tab delimiter - also add to the data matrix
for i = 1:nmarkers
    dataheader1 = [dataheader1 markers{i} '\t\t\t'];    
    dataheader2 = [dataheader2 'X' num2str(i) '\t' 'Y' num2str(i) '\t'...
        'Z' num2str(i) '\t'];
    format_text = [format_text '%f\t%f\t%f\t'];
    % add 3 rows of data for the X Y Z coordinates of the current marker
    % first check for NaN's and fill with a linear interpolant - warn the
    % user of the gaps
    clear m
    m = find(isnan(data.Markers.(markers{i})((data.Start_Frame:data.End_Frame),1))>0);
    if ~isempty(m)
        clear t d
        disp(['Warning -' markers{i} ' data missing in parts. Frames ' num2str(m(1)) '-'  num2str(m(end))])
        t = time;
        t(m) = [];
        d = data.Markers.(markers{i})((data.Start_Frame:data.End_Frame),:);
        d(m,:) = [];
        data.Markers.(markers{i})((data.Start_Frame:data.End_Frame),:) = interp1(t,d,time,'linear','extrap');
    end
    data_out = [data_out; data.Markers.(markers{i})((data.Start_Frame:data.End_Frame),:)'];
end
dataheader1 = [dataheader1 '\n'];
dataheader2 = [dataheader2 '\n'];
format_text = [format_text '\n'];

disp('Writing trc file...') 

%Output marker data to an OpenSim TRC file

newfilename = [fname '.trc'];

data.TRC_Filename = [newfilename];

%open the file
fid_1 = fopen([newfilename],'w');

% first write the header data
fprintf(fid_1,'PathFileType\t4\t(X/Y/Z)\t %s\n',newfilename);
fprintf(fid_1,'DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n');
fprintf(fid_1,'%d\t%d\t%d\t%d\t%s\t%d\t%d\t%d\n', data.Rate, data.Rate, nrows, nmarkers, data.units, data.Rate,data.Start_Frame,data.End_Frame); 
fprintf(fid_1, dataheader1);
fprintf(fid_1, dataheader2);

% then write the output marker data
fprintf(fid_1, format_text,data_out);

% close the file
fclose(fid_1);

disp('Done.')
end