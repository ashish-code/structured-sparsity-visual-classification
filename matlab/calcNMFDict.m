% compute NMF dictionary
function calcNMFDict(dataSet,dictType,dictSize,sampleSize)
% function calcNMFDict(dataSet,dictType,dictSize,sampleSize)
% dataSet : the data set utilized
% dictType: categorical; universal; balanced
% dictSize: number of elements in the dictionary
% sampleSize: the number of random samples used to compute the dictionary

rootDir = '/vol/vssp/diplecs/ash/Data/';
categoryListFileName = 'categoryList.txt';
sampleDir = '/collated/';
dictDir = '/Dictionary/';
optMode = 0; % 0 or 1 or 2;
SpamsMatlabPath = '/vol/vssp/diplecs/ash/Code/spams-matlab/';
cd (SpamsMatlabPath);
start_spams

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
    dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),num2str(sampleSize),'nmf','opt',num2str(optMode),'.dict'];
    fprintf('%s\n',sampleDataFile);
    % load the sample data file
    callNMF(sampleDataFile,dictDataFile,dictSize,optMode);
    fprintf('%s\n',sampleDataFile)
    
elseif strcmp(dictType,'categorical')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.cat'];
        dictDataFile = [(rootDir),(dataSet),(dictDir),(categoryList{iCategory}),num2str(dictSize),(dictType),num2str(sampleSize),'nmf','opt',num2str(optMode),'.dict'];
        fprintf('%s\n',sampleDataFile);
        callNMF(sampleDataFile,dictDataFile,dictSize,optMode);
        fprintf('%s\n',dictDataFile)
    end
elseif strcmp(dictType,'balanced')
    for iCategory = 1 : nCategory
        sampleDataFile = [(rootDir),(dataSet),(sampleDir),(categoryList{iCategory}),num2str(sampleSize),'.bal'];
        dictDataFile = [(rootDir),(dataSet),(dictDir),(categoryList{iCategory}),num2str(dictSize),(dictType),num2str(sampleSize),'nmf','opt',num2str(optMode),'.dict'];
        fprintf('%s\n',sampleDataFile);
        callNMF(sampleDataFile,dictDataFile,dictSize,optMode);
        fprintf('%s\n',dictDataFile)
    end
end

end

function callNMF(sampleDataFile,dictDataFile,dictSize,optMode)
% load the sample data file
    if exist(dictDataFile,'file')
        return;
    end
    sampleData = load(sampleDataFile);
    param.K = dictSize;
    param.iter = -10000;
    param.batchsize = 1000;
    param.modeParam = optMode;
    param.batch = true;
    param.numThreads = 4;
    [U V] = nmf(sampleData,param);  
    % write the dictionary to file
    dlmwrite(dictDataFile,U,'delimiter',',');
end