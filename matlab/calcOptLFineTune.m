function calcOptLFineTune(dataSet,dictType,dictSize,sampleSize,mode,modeD)
% function calcOptLambda(dataSet,dictType,dictSize,sampleSize,mode,modeD)
% dataSet : prefer VOC2006
% dictType : universal
% dictSize : 1000
% sampleSize : 200000
% mode : [0,1,2,3,4,5]
% modeD : [0,1,2]
% compute dictionary for different values of lambda and coefficients and
% subsequent classification performance.

rootDir = '/vol/vssp/diplecs/ash/Data/';
sampleDir = '/collated/';
dictDir = '/Dictionary/';

% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);

SpamsMatlabPath = '/vol/vssp/diplecs/ash/Code/spams-matlab/';
cd (SpamsMatlabPath);
start_spams


sampleDataFile = [(rootDir),(dataSet),(sampleDir),(dataSet),num2str(sampleSize),'.uni'];
% load the sample data file
sampleData = load(sampleDataFile);
fprintf('%s\n',sampleDataFile);

lambda = [50,100,200,400,600,1000,2000,4000];
for iLambda = 1 : max(size(lambda))
    
    dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),'dl','mode',num2str(mode),'modeD',num2str(modeD),'lambda',num2str(lambda(iLambda)),'.dict'];
    callDictLambda(dictDataFile,sampleData,dataSet,dictSize,mode,modeD,lambda(iLambda))
    callOMPCoeffNClassify(dictDataFile,dataSet,dictSize,mode,modeD,lambda(iLambda)); 
end

end

function callDictLambda(dictDataFile,sampleData,dataSet,dictSize,mode,modeD,lambda)
    if exist(dictDataFile,'file')
        return;
    end
    param.mode = mode;
    param.modeD = modeD;
    param.lambda = lambda;
    param.K = dictSize;
    param.iter = -7200;
    param.batchsize = 1000;
    param.posAlpha = false;
    param.posD = false;
    param.iter_updateD = 1;
    param.modeParam = 2;
    param.verbose = true;
    param.numThreads = -1;
    fprintf('computing %s\t%d\t%d\n',dataSet,lambda);
    [D] = mexTrainDL(sampleData,param);  
    % write the dictionary to file
    dlmwrite(dictDataFile,D,'delimiter',',');
    fprintf('written %s\n',dictDataFile);
end

function callOMPCoeffNClassify(dictDataFile,dataSet,dictSize,mode,modeD,lambda)
rootDir = '/vol/vssp/diplecs/ash/Data/';
imageListDir = '/ImageLists/';
coeffDir = '/Coeff/';
categoryListFileName = 'categoryList.txt';
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
lambdaDir = '/lambda/';
lambdaPerFileAvg = [(rootDir),(dataSet),(lambdaDir),'mode',num2str(mode),'modeD',num2str(modeD),'lambda',num2str(lambda),'.avg'];

lambdaAvg = zeros(nCategory,3);


for iCategory = 1 : nCategory
    % load the images from imagelist
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
        
        FTrainPosAvg = ones(nListTrainPos,dictSize+1);
        FTrainNegAvg = zeros(nListTrainNeg,dictSize+1);
        FValPosAvg = ones(nListValPos,dictSize+1);
        FValNegAvg = zeros(nListValNeg,dictSize+1);        
        
        % Train ; Pos
        for iter = 1 : nListTrainPos
            imageName = listTrainPos{iter};
            Favg = callOMPnClassify(imageName,dict,dataSet,dictSize);          
            if size(Favg,1) > size(Favg,2)
                Favg = Favg';
            end                 
            FTrainPosAvg(iter,1:dictSize) = Favg;            
        end
        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            Favg = callOMPnClassify(imageName,dict,dataSet,dictSize);
            if size(Favg,1) > size(Favg,2)
                Favg = Favg';
            end            
            FValPosAvg(iter,1:dictSize) = Favg;           
        end
        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            Favg = callOMPnClassify(imageName,dict,dataSet,dictSize);
            if size(Favg,1) > size(Favg,2)
                Favg = Favg';
            end           
            FTrainNegAvg(iter,1:dictSize) = Favg;            
        end
        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            Favg= callOMPnClassify(imageName,dict,dataSet,dictSize);
            if size(Favg,1) > size(Favg,2)
                Favg = Favg';
            end            
            FValNegAvg(iter,1:dictSize) = Favg;          
        end
    end
    
    FTrainAvg = [FTrainPosAvg;FTrainNegAvg];
    FValAvg = [FValPosAvg;FValNegAvg];
      
    

    %---------------------------------------------------------------------
    % CLASSIFICATION
    %---------------------------------------------------------------------
    % echo pipeline stage: classification
    fprintf('%s\n','classification');

    cdir = pwd;
    cd '/vol/vssp/diplecs/ash/code/libsvm-3.11/matlab/';
    % train the classifier
    svmStruct = svmtrain(FTrainAvg(:,dictSize+1),FTrainAvg(:,1:dictSize), '-h 0');
    % predict label of data using the trained classifier
    [predLabel, ~, predValues] = svmpredict(FValAvg(:,dictSize+1), FValAvg(:,1:dictSize), svmStruct);
    cd (cdir);

    [~, ~, ~, averagePrecision] = precisionRecall(predValues, FValAvg(:,dictSize+1), 'r');
    [~, ~, AUC] = ROCcurve(predValues, FValAvg(:,dictSize+1));
    cp = classperf(FValAvg(:,dictSize+1),predLabel);
    fprintf('%s\t%f\t%f\n',categoryList{iCategory},averagePrecision,AUC);
    
    lambdaAvg(iCategory,1) = averagePrecision;
    lambdaAvg(iCategory,2) = AUC;
    lambdaAvg(iCategory,3) = cp.CorrectRate;       
    
end % end for category loop

% write the performance for each lambda to file
dlmwrite(lambdaPerFileAvg,lambdaAvg,'delimiter',',');

end % end calcOpt func call

function Favg = callOMPnClassify(imageName,dict,dataSet,dictSize)
    rootDir = '/vol/vssp/diplecs/ash/Data/';
    dsiftDir = '/DSIFT/';
    imageFilePath = [(rootDir),(dataSet),(dsiftDir),(imageName),'.dsift'];
    imageData = load(imageFilePath);
    imageData = imageData(3:130,:);    
    nNonZero = ceil(0.8*dictSize); % 20 percent 0 coeffs    
    params.L = nNonZero;
    params.numThreads = -1;
    alpha = mexOMP(imageData,dict,params);
    coeff = full(alpha);    
    Favg = mean(coeff,2);    
end
