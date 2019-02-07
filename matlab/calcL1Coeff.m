% calculate l1 coeff for comparison with gltopiccoeff
function calcL1Coeff(dataSet,algo,param,method)
% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);

dictType = 'universal';
dictSize = 1000;
sampleSize = 100000;

rootDir = '/vol/vssp/diplecs/ash/Data/';
coeffDir = '/Coeff/';
categoryListFileName = 'categoryList.txt';
dictDir = '/Dictionary/';
imageListDir = '/ImageLists/';

%---------------------------------------------------------------------
% paths to data directories
paths.rootDir = '/vol/vssp/diplecs/ash/Data/';
paths.sampleDir = '/collated/';
paths.dictDir = '/Dictionary/';
paths.coclustDir = '/CoClust/';
paths.coeffDir = '/Coeff/';
paths.dsiftDir = '/DSIFT/';
paths.SLEPDir = '/vol/vssp/diplecs/ash/code/SLEP/';

%---------------------------------------------------------------------
params.dataSet = dataSet;
params.dictType = dictType;
params.dictSize = num2str(dictSize);
params.sampleSize = num2str(sampleSize);
params.algo = algo;
params.algoParam = param;
params.categoryListFileName = 'categoryList.txt';
params.imageListDir = '/ImageLists/';
params.listSize = 30;
params.method = method;
%

% read the category list in the dataset
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath);
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
params.categoryList = categoryList;
%
nCategory = size(categoryList,1);
listSizes = 30;
nListSizes = max(size(listSizes));
%

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
    
    % read topic co-cluster file
%     ccFilePath = strcat(paths.rootDir,params.dataSet,paths.coclustDir,params.categoryList{iCategory},num2str(params.dictSize),params.dictType,num2str(params.sampleSize),params.algo,num2str(params.algoParam),params.method,params.ccType,num2str(params.rowClust),num2str(params.colClust),'.t');
%     try
%         ccfid = fopen(ccFilePath);
%     catch err
%         fprintf('%s\n',err.identifier);
%         return;
%     end
%         
%     rowcc = fgetl(ccfid);
%     clear rowcc;
%     colcc = fgetl(ccfid);
%     colcc = textscan(colcc,'%d ');
%     fclose(ccfid);
%     colcc = colcc{1};
%     [ccSort,ccIdx] = sort(colcc);
%     ccUnique = unique(ccSort);
%     % ind(i)+1 -> ind(i+1); ind array begins with 0
%     ind = zeros(1,1+max(size(ccUnique)));
%     for i = 1 : max(size(ccUnique))
%         ind(i+1) = max(find(ccSort == ccUnique(i)));
%     end
    
    % rearrange the columns of dictionary matrix
%     dict = dict(:,ccIdx);
%         

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
        
        % Train ; Pos
        for iter = 1 : nListTrainPos
            imageName = listTrainPos{iter};
            callGroupLasso(imageName,dict,paths,params);            
        end
        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            callGroupLasso(imageName,dict,paths,params);           
        end
        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            callGroupLasso(imageName,dict,paths,params);           
        end
        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            callGroupLasso(imageName,dict,paths,params);         
        end
    end
end

end

function callGroupLasso(imageName,dict,paths,params)
    coeffFilePathAvg = strcat(paths.rootDir,params.dataSet,paths.coeffDir,imageName,num2str(params.dictSize),params.dictType,params.algo,num2str(params.algoParam),params.method,'.l1');
%     if exist(coeffFilePathAvg,'file')
%         return;
%     end
    addpath(genpath([(paths.SLEPDir) '/SLEP']));
    
    % read image data
    imageFilePath = strcat(paths.rootDir,params.dataSet,paths.dsiftDir,imageName,'.dsift');
    imageData = load(imageFilePath);
    imageData = imageData(3:130,:);
    
    dictSize = size(dict,2);
    ind = 0:dictSize;
    
    % ----------------------------------------------------------------
    
    k=length(ind)-1;     % number of groups
    q=2;                 % the value of q in the L1/Lq regularization
    rho=0.1;             % the regularization parameter

    randNum=1;           % a random number
    
    %----------------------- Set optional items -----------------------
    opts=[];

    % Starting point
    opts.init=2;        % starting from a zero point

    % Termination 
    opts.tFlag=5;       % run .maxIter iterations
    opts.maxIter=200;   % maximum number of iterations

    % Normalization
    opts.nFlag=0;       % without normalization

    % Regularization
    opts.rFlag=1;       % the input parameter 'rho' is a ratio in (0, 1)

    % Group Property
    opts.ind=ind;       % set the group indices
    opts.q=q;           % set the value for q
    opts.sWeight=[1,1]; % set the weight for positive and negative samples
    opts.gWeight=ones(k,1); % set the weight for the group, a cloumn vector
    
    % ----------------------------------------------------------------
    
    %----------------------- Run the code glLeastR -----------------------
    fprintf('\n mFlag=0, lFlag=0 \n');
    opts.mFlag=0;       % treating it as compositive function 
    opts.lFlag=0;       % Nemirovski's line search
    tic;
    [coeff, funVal1, ValueL1]= mcLeastR(dict, imageData, rho, opts);
    toc;
    Favg = mean(coeff,2);
    
    dlmwrite(coeffFilePathAvg,Favg,'delimiter',',');
    fprintf('%s\n',coeffFilePathAvg);    
end
