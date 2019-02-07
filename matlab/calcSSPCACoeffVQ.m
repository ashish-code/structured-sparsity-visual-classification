% calc sspca coeff using vector quantization

function calcSSPCACoeffVQ(dataSet,ccType,rowClust,colClust)
dictType = 'universal';
dictSize = 1000;
algo = 'sspca';
param = '';

% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);

rootDir = '/vol/vssp/diplecs/ash/Data/';
categoryListFileName = 'categoryList.txt';
dictDir = '/Dictionary/';
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

% loop over each category to compute its decomposition coefficient
% according the dictionary specified

for iCategory = 1 : nCategory
    % load the images from imagelist    
    dictDataFile = strcat(rootDir,dataSet,dictDir,dataSet,dictType,num2str(dictSize),algo,num2str(rowClust),num2str(colClust),ccType,'.dict');
    dict = load(dictDataFile);
    if ismember(dataSet,['Scene15','Caltech101','Caltech256'])
        coeffCatDir = [(rootDir),(dataSet),(coeffDir),categoryList{iCategory}];
        if exist(coeffCatDir,'dir') ~= 7
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
            callVQEnc(imageName,dict,dataSet,dictType,dictSize,algo,param,ccType,rowClust,colClust);            
        end
        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            callVQEnc(imageName,dict,dataSet,dictType,dictSize,algo,param,ccType,rowClust,colClust);           
        end
        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            callVQEnc(imageName,dict,dataSet,dictType,dictSize,algo,param,ccType,rowClust,colClust);           
        end
        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            callVQEnc(imageName,dict,dataSet,dictType,dictSize,algo,param,ccType,rowClust,colClust);         
        end
    end
end

end

function callVQEnc(imageName,dict,dataSet,dictType,dictSize,algo,param,ccType,rowClust,colClust)
rootDir = '/vol/vssp/diplecs/ash/Data/';
coeffDir = '/Coeff/';
dsiftDir = '/DSIFT/';

% to conform with the nomenclature of OMP and Lasso
method = 'VQ';

coeffFilePathAvg = [(rootDir),(dataSet),(coeffDir),imageName,(dictType),(algo),num2str(param),(method),num2str(rowClust),num2str(colClust),ccType,'.avg'];
if exist(coeffFilePathAvg,'file')
    return;
end

imageFilePath = [(rootDir),(dataSet),(dsiftDir),(imageName),'.dsift'];
imageData = load(imageFilePath);
imageData = imageData(3:130,:);

hvqenc = dsp.VectorQuantizerEncoder('Codebook',dict,'CodewordOutputPort', false,'QuantizationErrorOutputPort', false, 'OutputIndexDataType', 'uint16');
idx = step(hvqenc,imageData);
idx = idx+1;
coeff = zeros(dictSize,size(imageData,2));
for i = 1 : size(imageData,2)
    coeff(idx(i),i) = 1;
end
Favg = mean(coeff,2);
dlmwrite(coeffFilePathAvg,Favg,'delimiter',',');
fprintf('%s\n',coeffFilePathAvg);

end