% dimensionality reduction
function calcMapping(dataSet,dictType,sampleSize)
% function calcSubSpace(dataSet,dictType,sampleSize)

% initialize matlab
cdir = pwd;
cd ~
startup;
cd (cdir)

% paths
rootDir = '/vol/vssp/diplecs/ash/Data/';

categoryListFileName = 'categoryList.txt';
sampleDir = '/collated/';
mappingDir = '/Mapping/';
intDimDir = '/IntDim/';

methods = {
 'PCA';
 'LDA';
 'MDS';
 'ProbPCA';
 'FactorAnalysis';
%'Sammon';
 'Isomap';         
 'LandmarkIsomap';
 'LLE';            
%'Laplacian';       
%'HessianLLE'; 
%'LTSA';                   
 'DiffusionMaps';
 'KernelPCA';
%'KernelLDA';
%'SNE';
 'SymSNE';
 'tSNE';
 'NPE';
 'LPP';
 'SPE';
% 'LLTSA';
%'CCA';
%'MVU';
%'LandmarkMVU';
%'FastMVU';
%'LLC';
%'ManifoldChart';
%'CFA';
%'GPLVM';
%'AutoEncoderRBM';
%'AutoEncoderEA';
%'NCA';
%'MCML';
};
nMethods = size(methods,1);

% read the category list in the dataset
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath);
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
%
nCategory = size(categoryList,1);

intDimMethod = 'MLE';

if strcmp(dictType,'universal')
    sampleDataFile = [(rootDir),(dataSet),(sampleDir),(dataSet),num2str(sampleSize),'.uni'];
    intDimFile = [(rootDir),(dataSet),(intDimDir),(dataSet),(dictType),intDimMethod,'.dim'];
    
    fprintf('%s\n',sampleDataFile);
    % load the sample data file
    for iMethod = 1 : nMethods
        method = methods{iMethod};
        mappingFile = [(rootDir),(dataSet),(mappingDir),(dataSet),(dictType),intDimMethod,method,'.mat'];
        callMapping(sampleDataFile,intDimFile,mappingFile,method);
        fprintf('%s\n',mappingFile);
    end   
    
elseif strcmp(dictType,'categorical')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.cat'];
        intDimFile = [(rootDir),(dataSet),(intDimDir),(categoryList{iCategory}),(dictType),intDimMethod,'.dim'];
        
        fprintf('%s\n',sampleDataFile);
        for iMethod = 1 : nMethods
            method = methods{iMethod};
            mappingFile = [(rootDir),(dataSet),(mappingDir),(categoryList{iCategory}),(dictType),intDimMethod,method,'.mat'];
            callMapping(sampleDataFile,intDimFile,mappingFile,method);
            fprintf('%s\n',mappingFile);
        end
        
    end
elseif strcmp(dictType,'balanced')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.bal'];
        intDimFile = [(rootDir),(dataSet),(intDimDir),(categoryList{iCategory}),(dictType),intDimMethod,'.dim'];
        
        fprintf('%s\n',sampleDataFile);
        for iMethod = 1 : nMethods
            method = methods{iMethod};
            mappingFile = [(rootDir),(dataSet),(mappingDir),(categoryList{iCategory}),(dictType),intDimMethod,method,'.mat'];
            callMapping(sampleDataFile,intDimFile,mappingFile,method);
            fprintf('%s\n',mappingFile);
        end
        
    end
end
end

function callMapping(sampleDataFile,intDimFile,mappingFile,method)

if exist(mappingFile,'file')
    return;
end
sampleData = load(sampleDataFile);
sampleData = sampleData';
nVec = size(sampleData,1);

% Due to high computational cost of graph and local neighborhood based
% methods, the number of samples is kept different

if ismember(method,['PCA','LDA','MDS','FactorAnalysis','LandmarkIsomap','LPP'])
    nSample = 1000;
else
    nSample = 200;
end

rndSample = randsample(nVec,nSample);
sample = sampleData(rndSample,:);

intDimData = load(intDimFile);
intDim = uint16(round(intDimData(1)));
fprintf('method: %s\t intDim: %d',method,intDim);
[~,sampleMapping] = compute_mapping(sample,method,intDim);
save(mappingFile,'-struct','sampleMapping');


end