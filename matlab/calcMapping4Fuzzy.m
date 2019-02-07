% dimensionality reduction
function calcMapping4Fuzzy(dataSet,dictType,sampleSize,intDim)
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

% methods = {
%  'PCA';
%  'MDS';
%  'ProbPCA';
%  'LPP';
%  'Isomap';
%  'LLE';
%  'NPE'
% };

methods = {'PCA'};

nMethods = size(methods,1);

% read the category list in the dataset
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath);
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
%
nCategory = size(categoryList,1);

if strcmp(dictType,'universal')
    sampleDataFile = [(rootDir),(dataSet),(sampleDir),(dataSet),num2str(sampleSize),'.uni'];
    fprintf('%s\n',sampleDataFile);
    % load the sample data file
    for iMethod = 1 : nMethods
        method = methods{iMethod};
        mappingFile = [(rootDir),(dataSet),(mappingDir),(dataSet),(dictType),method,num2str(intDim),'.mat'];
        callMapping(sampleDataFile,intDim,mappingFile,method);
        fprintf('%s\n',mappingFile);
    end   
    
elseif strcmp(dictType,'categorical')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.cat'];
        fprintf('%s\n',sampleDataFile);
        for iMethod = 1 : nMethods
            method = methods{iMethod};
            mappingFile = [(rootDir),(dataSet),(mappingDir),(categoryList{iCategory}),(dictType),method,num2str(intDim),'.mat'];
            callMapping(sampleDataFile,intDim,mappingFile,method);
            fprintf('%s\n',mappingFile);
        end
        
    end
elseif strcmp(dictType,'balanced')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.bal'];
        fprintf('%s\n',sampleDataFile);
        for iMethod = 1 : nMethods
            method = methods{iMethod};
            mappingFile = [(rootDir),(dataSet),(mappingDir),(categoryList{iCategory}),(dictType),method,num2str(intDim),'.mat'];
            callMapping(sampleDataFile,intDim,mappingFile,method);
            fprintf('%s\n',mappingFile);
        end
        
    end
end
end

function callMapping(sampleDataFile,intDim,mappingFile,method)

if exist(mappingFile,'file')
    return;
end
sampleData = load(sampleDataFile);
sampleData = sampleData';
nVec = size(sampleData,1);

nSample = 10000;

rndSample = randsample(nVec,nSample);
sample = sampleData(rndSample,:);

fprintf('method: %s\t intDim: %d',method,intDim);
[~,sampleMapping] = compute_mapping(sample,method,intDim);
save(mappingFile,'-struct','sampleMapping');


end