function ccssprojcoeff(dataSet,dictSize,colClust,ccType)
dictType = 'universal';
sampleSize = 100000;
rowClust = colClust;
%---------------------------------------------------------------------
% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);
%---------------------------------------------------------------------
% paths to data directories
paths.rootDir = '/vol/vssp/diplecs/ash/Data/';
paths.sampleDir = '/collated/';
paths.dictDir = '/Dictionary/';
paths.coclustDir = '/CoClust/';
paths.coeffDir = '/Coeff/';
paths.imageListDir = '/ImageLists/';
paths.tempDir = 'Temp/';
%---------------------------------------------------------------------
params.dataSet = dataSet;
params.dictType = dictType;
params.dictSize = dictSize;
params.sampleSize = sampleSize;
params.categoryListFileName = 'categoryList.txt';
params.rowClust = rowClust;
params.colClust = colClust;
params.ccType = ccType;
params.progPath = '/vol/vssp/diplecs/ash/code/cocluster/';
params.prog = 'cocluster-linux';

% ccfilepath
tempCCFilePath = strcat(paths.rootDir,params.dataSet,paths.coclustDir,params.dataSet,num2str(params.dictSize),params.dictType,num2str(params.sampleSize),params.ccType,num2str(params.rowClust),num2str(params.colClust),'.s');
%---------------------------------------------------------------------
sampleDataFile = [(paths.rootDir),(params.dataSet),(paths.sampleDir),(params.dataSet),num2str(params.sampleSize),'.uni'];
sampleData = load(sampleDataFile);
fprintf('%s loaded\n',sampleDataFile);

nVec = size(sampleData,2);
nSample = 10000;
rndSample = randsample(nVec,nSample);
sampleData = sampleData(:,rndSample);

tempTimeDir = strcat(num2str(floor(now*10000000)),'/');
tempPath = strcat(paths.rootDir,paths.tempDir,tempTimeDir);
if ~exist(tempPath,'dir')
    mkdir(tempPath);
end
tempDataPath = strcat(tempPath,'tempdata');
if ~exist(tempDataPath,'file')
    dlmwrite(tempDataPath,sampleData,' ');
end
tempDataDimPath = strcat(tempPath,'tempdata_dim');
dataDim = size(sampleData)';
if ~exist(tempDataDimPath,'file')
    fid = fopen(tempDataDimPath,'w');
    fprintf(fid,'%s\n%s',num2str(dataDim(1)),num2str(dataDim(2)));
    fclose(fid);
end
progArgs = sprintf(' -A %s -R %d -C %d -I d s %s -O c s 0 o %s',params.ccType,params.rowClust,params.colClust,tempDataPath,tempCCFilePath);
cmd = strcat(params.progPath,params.prog,progArgs);
% system call to cocluster linux program
fprintf('%s\n','co-clustering...');
system(cmd);
if exist(tempCCFilePath,'file')
    fprintf('%s written\n',tempCCFilePath);
    rmdir(tempPath,'s');    
else
    fprintf('%s ERROR\n',tempCCFilePath);
end

ccFilePath = strcat(paths.rootDir,params.dataSet,paths.coclustDir,params.dataSet,num2str(params.dictSize),params.dictType,num2str(params.sampleSize),params.ccType,num2str(params.rowClust),num2str(params.colClust),'.s');
disp(ccFilePath);
try
    ccfid = fopen(ccFilePath);
    
catch err
    fprintf('%s, %s','unable to open ',ccFilePath);
    fprintf('%s\n',err.identifier);
    return;
end

% rowcc = fgetl(ccfid);
colcc = fgetl(ccfid);
fclose(ccfid);

% rowcc = textscan(rowcc,'%d ');
colcc = textscan(colcc,'%d ');

% rowcc = rowcc{1};
colcc = colcc{1};

% rowcc = rowcc+1;
colcc = colcc+1;

% [rowSort,rowIdx] = sort(rowcc);
[colSort,colIdx] = sort(colcc);

colUnique = unique(colSort);

dictFilePath = strcat(paths.rootDir,params.dataSet,paths.dictDir,params.dataSet,num2str(params.dictSize),params.dictType,num2str(params.sampleSize),'kmeans','.dict');

if exist(dictFilePath,'file')
    dict = dlmread(dictFilePath,',');
    dict = dict';
else
    fprintf('%s\n','computing dictionary...');
    opts = statset('MaxIter',20);    
    [~, dict] = kmeans(sampleData,dictSize,'Start','cluster','EmptyAction','singleton','Options',opts);          
    dlmwrite(dictDataFile,dict','delimiter',',');
end

dict = dict(:,colIdx);


% find the maximum size
% colSort ; colUnique
nSubspace = max(size(colUnique));

% for each dictionary element, each vector in the dictionary
dictsubspace = zeros(size(dict,1),params.colClust);
for iDict = 1 : params.dictSize
    % compute
    dvec = dict(iDict,:);
    %
    normvec = zeros(nSubspace,1);
    for iSS = 1 : nSubspace
        dvecss = dvec(find(colSort == colUnique(iSS)));
        normvec(iSS) = norm(dvecss,2);
        dictsubspace(iDict,iSS) = normvec(iSS);
    end
end

%
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%

dict = dictsubspace;

LASTN = maxNumCompThreads('automatic');
fprintf('%s\t%d\n','numThreads',LASTN);

rootDir = '/vol/vssp/diplecs/ash/Data/';
categoryListFileName = 'categoryList.txt';

imageListDir = '/ImageLists/';
coeffDir = '/Coeff/';
% read the category list in the dataset
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath,'r');
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
%
nCategory = size(categoryList,1);
listSizes = 30;
nListSizes = max(size(listSizes));
%
for iCategory = 1 : nCategory      
    if ismember(dataSet,['Scene15','Caltech101','Caltech256'])
        coeffCatDir = [(rootDir),(dataSet),(coeffDir),categoryList{iCategory}];
        if exist(coeffCatDir,'dir') ~= 7
            mkdir(coeffCatDir)
        end
    end
    %
    for iListSize = 1 : nListSizes
        listTrainPosFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Train',num2str(listSizes(iListSize)),'.pos'];
        listValPosFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Val',num2str(listSizes(iListSize)),'.pos'];
        listTrainNegFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Train',num2str(listSizes(iListSize)),'.neg'];
        listValNegFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Val',num2str(listSizes(iListSize)),'.neg'];
        %        
        fid = fopen(listTrainPosFile,'r');
        listTrainPos = textscan(fid,'%s');
        fclose(fid);
        listTrainPos = listTrainPos{1};
        %
        fid = fopen(listValPosFile,'r');
        listValPos = textscan(fid,'%s');
        fclose(fid);
        listValPos = listValPos{1};
        %
        fid = fopen(listTrainNegFile,'r');
        listTrainNeg = textscan(fid,'%s');
        fclose(fid);
        listTrainNeg = listTrainNeg{1};
        %
        fid = fopen(listValNegFile,'r');
        listValNeg = textscan(fid,'%s');
        fclose(fid);
        listValNeg = listValNeg{1};
        %
        nListTrainPos = size(listTrainPos,1);
        nListValPos = size(listValPos,1);
        nListTrainNeg = size(listTrainNeg,1);
        nListValNeg = size(listValNeg,1);         
        % Train ; Pos
        for iter = 1 : nListTrainPos
            imageName = listTrainPos{iter};
            callSubspaceVQEnc(imageName,dict,dataSet,dictType,dictSize,ccType,colClust,colIdx,colSort);            
        end        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            callSubspaceVQEnc(imageName,dict,dataSet,dictType,dictSize,ccType,colClust,colIdx,colSort);           
        end        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            callSubspaceVQEnc(imageName,dict,dataSet,dictType,dictSize,ccType,colClust,colIdx,colSort);           
        end        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            callSubspaceVQEnc(imageName,dict,dataSet,dictType,dictSize,ccType,colClust,colIdx,colSort);         
        end
    end
end

end

function callSubspaceVQEnc(imageName,dict,dataSet,dictType,dictSize,ccType,colClust,colIdx,colSort)
rootDir = '/vol/vssp/diplecs/ash/Data/';
coeffDir = '/Coeff/';
dsiftDir = '/DSIFT/';
%
coeffFilePathAvg = [(rootDir),(dataSet),(coeffDir),imageName,num2str(dictSize),(dictType),num2str(colClust),ccType,'.ssproj'];
if exist(coeffFilePathAvg,'file')
    return;
end
%
imageFilePath = [(rootDir),(dataSet),(dsiftDir),(imageName),'.dsift'];
imageData = load(imageFilePath);
imageData = imageData(3:130,:);
imageData = imageData';
colUnique = unique(colSort);
nSubspace = max(size(colUnique));
imageData = imageData(:,colIdx);
imgsubspace = zeros(size(imageData,1),colClust);
for i = 1 : size(imageData,1);
    % compute
    dvec = imageData(i,:);
    %    
    for iSS = 1 : nSubspace
        dvecss = dvec(find(colSort == colUnique(iSS)));        
        imgsubspace(i,iSS) = norm(dvecss,2);
    end
end
imageData = imgsubspace;
nVec = size(imageData,1);
%
coeff = zeros(1,dictSize);
% for each vector in an image

for i = 1 : nVec
    % for each dictionary element
    dd = zeros(1,dictSize);
    for j = 1 : dictSize        
        dd(j) = norm(imageData(i,:)-dict(j,:));
    end
    didx = find(dd == min(dd));
    coeff(didx) = coeff(didx) + 1;
end
coeff = coeff./sum(coeff);

dlmwrite(coeffFilePathAvg,coeff,'delimiter',',');
fprintf('%s\n',coeffFilePathAvg);

end