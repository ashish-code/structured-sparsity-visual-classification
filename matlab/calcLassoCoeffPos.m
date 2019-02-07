% calculate lasso coeff positive
function calcLassoCoeffPos(dataSet,dictType,dictSize,sampleSize,algo,param)
cdir = pwd;
cd ~;
startup;
cd (cdir);

SpamsMatlabPath = '/vol/vssp/diplecs/ash/Code/spams-matlab/';
cd (SpamsMatlabPath);
start_spams

rootDir = '/vol/vssp/diplecs/ash/Data/';
coeffDir = '/Coeff/';
categoryListFileName = 'categoryList.txt';
dictDir = '/Dictionary/';
imageListDir = '/ImageLists/';

% read the category list in the dataset
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath);
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
%
nCategory = size(categoryList,1);
listSizes = 30;
nListSizes = max(size(listSizes));
%


% loop over each category to compute its decomposition coefficient
% according the dictionary specified

for iCategory = 1 : nCategory
    % load the images from imagelist
    if strcmp(dictType,'universal')
        dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),num2str(sampleSize),algo,num2str(param),'.dict'];
    elseif ismember(dictType,['categorical','balanced'])
        dictDataFile = [(rootDir),(dataSet),(dictDir),(categoryList{iCategory}),num2str(dictSize),(dictType),num2str(sampleSize),algo,num2str(param),'.dict'];
    end
    dict = load(dictDataFile);
    if ~ismember(dataSet,['VOC2006','VOC2007','VOC2010'])
        coeffCatDir = [(rootDir),(dataSet),(coeffDir),categoryList{iCategory},'/'];
        if ~exist(coeffCatDir,'dir')
            mkdir(coeffCatDir)
        end
    end
    for iListSize = 1 : nListSizes
        listTrainPosFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Train',num2str(listSizes(iListSize)),'.pos'];
        listValPosFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Val',num2str(listSizes(iListSize)),'.pos'];
        listTrainNegFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Train',num2str(listSizes(iListSize)),'.neg'];
        listValNegFile = [(rootDir),(dataSet),(imageListDir),categoryList{iCategory},'Val',num2str(listSizes(iListSize)),'.neg'];
        
        fid = fopen(listTrainPosFile,'r');
        listTrainPos = textscan(fid,'%s');
        fclose(fid);
        listTrainPos = listTrainPos{1};
        
        fid = fopen(listValPosFile,'r');
        listValPos = textscan(fid,'%s');
        fclose(fid);
        listValPos = listValPos{1};
        
        fid = fopen(listTrainNegFile,'r');
        listTrainNeg = textscan(fid,'%s');
        fclose(fid);
        listTrainNeg = listTrainNeg{1};
        
        fid = fopen(listValNegFile,'r');
        listValNeg = textscan(fid,'%s');
        fclose(fid);
        listValNeg = listValNeg{1};
        
        nListTrainPos = size(listTrainPos,1);
        nListValPos = size(listValPos,1);
        nListTrainNeg = size(listTrainNeg,1);
        nListValNeg = size(listValNeg,1);
        
        % DEBUG
        
        
        % Train ; Pos
        for iter = 1 : nListTrainPos
            imageName = listTrainPos{iter};
            callLasso(imageName,dict,dataSet,dictType,dictSize,sampleSize,algo,param);            
        end
        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            callLasso(imageName,dict,dataSet,dictType,dictSize,sampleSize,algo,param);           
        end
        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            callLasso(imageName,dict,dataSet,dictType,dictSize,sampleSize,algo,param);           
        end
        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            callLasso(imageName,dict,dataSet,dictType,dictSize,sampleSize,algo,param);         
        end
    end
end

end

function callLasso(imageName,dict,dataSet,dictType,dictSize,sampleSize,algo,param)
    rootDir = '/vol/vssp/diplecs/ash/Data/';
    coeffDir = '/Coeff/';
    dsiftDir = '/DSIFT/';
    method = 'Lasso';
    
    imageFilePath = strcat(rootDir,dataSet,dsiftDir,imageName,'.dsift');
    imageData = load(imageFilePath);
    imageData = imageData(3:130,:);
    
    params.mode = 0;
    params.pos = true;
    params.lambda = 10;
    params.numThreads = -1;
    
    alpha = mexLasso(imageData,dict,params);
    coeff = full(alpha);   
    Favg = mean(coeff,2);    
    coeffFilePathAvg = [(rootDir),(dataSet),(coeffDir),imageName,num2str(dictSize),(dictType),num2str(sampleSize),(algo),num2str(param),(method),num2str(dictSize),'.avg'];
        
    dlmwrite(coeffFilePathAvg,Favg,'delimiter',',');
    fprintf('%s\n',coeffFilePathAvg);       
end