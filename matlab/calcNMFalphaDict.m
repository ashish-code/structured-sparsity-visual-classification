function calcNMFalphaDict(dataSet,alpha)
% function calcNMFDict(dataSet,dictType,dictSize,sampleSize)

dictSize = 1000;
dictType = 'universal';
sampleSize = 100000;

rootDir = '/vol/vssp/diplecs/ash/Data/';
sampleDir = '/collated/';
dictDir = '/Dictionary/';

sampleDataFile = [(rootDir),(dataSet),(sampleDir),(dataSet),num2str(sampleSize),'.uni'];
dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),num2str(sampleSize),'nmf','alpha',num2str(alpha),'.dict'];

% load the sample data file
callNMFalpha(sampleDataFile,dictDataFile,dictSize,alpha);
fprintf('%s\n',sampleDataFile)

end

function callNMFalpha(sampleDataFile,dictDataFile,dictSize,alpha)
    progDir = '/vol/vssp/diplecs/ash/code/nmflib/';
    sampleData = load(sampleDataFile);    
    rndIdx = randsample(size(sampleData,2)-1,4000);
    sampleData = sampleData(:,rndIdx);
    cd (progDir);
    disp('compute dict...');
    tic;
    % W is not normalized
    % H is l1 normalized
    [D,~,~,~] = nmf_amari(sampleData,dictSize,'alpha',alpha,'niter',20000,'norm_w',0,'norm_h',0,'verb',3);
    toc;
    dlmwrite(dictDataFile,D,'delimiter',',');
    fprintf('%s\n',dictDataFile);
end