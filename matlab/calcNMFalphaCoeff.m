% compute NMF alpha coefficients
function calcNMFalphaCoeff(dataSet,alpha)
sampleSize = 100000;
algo = 'nmfalpha';
dictSize = 1000;
dictType = 'universal';

cdir = pwd;
cd ~;
startup;
cd (cdir);

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

for iCategory = 1 : nCategory
    % load the images from imagelist
    if strcmp(dictType,'universal')
        dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),num2str(sampleSize),algo,num2str(alpha),'.dict'];
    elseif ismember(dictType,['categorical','balanced'])
        dictDataFile = [(rootDir),(dataSet),(dictDir),(categoryList{iCategory}),num2str(dictSize),(dictType),num2str(sampleSize),algo,num2str(alpha),'.dict'];
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
               
        % Train ; Pos
        for iter = 1 : nListTrainPos
            imageName = listTrainPos{iter};
            callnmfalpha(imageName,dict,dataSet,dictSize,algo,alpha);            
        end
        
        % Val ; Pos
        for iter = 1 : nListValPos
            imageName = listValPos{iter};
            callnmfalpha(imageName,dict,dataSet,dictSize,algo,alpha);           
        end
        
        % Train ; Neg
        for iter = 1 : nListTrainNeg
            imageName = listTrainNeg{iter};
            callnmfalpha(imageName,dict,dataSet,dictSize,algo,alpha);           
        end
        
        % Val ; Neg
        for iter = 1 : nListValNeg
            imageName = listValNeg{iter};
            callnmfalpha(imageName,dict,dataSet,dictSize,algo,alpha);         
        end
    end
end

end

function callnmfalpha(imageName,dict,dataSet,dictSize,algo,alpha)
rootDir = '/vol/vssp/diplecs/ash/Data/';
    coeffDir = '/Coeff/';
    dsiftDir = '/DSIFT/';
    
    imageFilePath = strcat(rootDir,dataSet,dsiftDir,imageName,'.dsift');
    imageData = load(imageFilePath);
    imageData = imageData(3:130,:);
    
    coeffFilePathAvg = [(rootDir),(dataSet),(coeffDir),imageName,(algo),num2str(alpha),'.avg'];
    [dict,H,~,~] = nmf_amari(imageData,dictSize,'alpha',alpha,'niter',50,'norm_w',0,'norm_h',1,'verb',3);
    disp(size(dict));
    disp(H);
    disp(size(H));
    Favg = mean(H,2);
    disp(size(Favg));
    dlmwrite(coeffFilePathAvg,Favg,'delimiter',',');    
    fprintf('%s\n',coeffFilePathAvg);
    
end