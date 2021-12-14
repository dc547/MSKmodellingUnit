function modelOutputPath = strengthScaler_AllMuscles(modelPath,muscles_num,n,resultsFolder,addName)

%%muscles_num --> nMUS=OSmodel.getMuscles() and then nMUS.getSize()

% Import OpenSim Libraries
import org.opensim.modeling.*      

if nargin < 4
    resultsFolder = 'Results';
end

[pathName, modelName, ext] = fileparts(modelPath); 

% create instance of the model 
myModel = Model(modelPath);
myModel.initSystem();

% make the scaling factor a decimal (if 100% then 1, if 50% then 0.5
scalingFactor = n/100;

% multiply muscles -found in muscleList- in the model by scalingFactor
for ii = 0 : muscles_num-1
    b = myModel.getMuscles.get( ii ).getMaxIsometricForce ;
    myModel.getMuscles.get( ii ).setMaxIsometricForce( b*scalingFactor ) ;
end

% Print the model out to the results file, ready to be used by the
% cmcTool
modelOutputPath = fullfile(resultsFolder, ['myModel_' addName '_' num2str(round(n)) '.osim']) ;
myModel.print(modelOutputPath);

display('model printed')

end 
