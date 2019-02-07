function calcNMFbetaDict(dataSet,beta)
% function calcNMFDict(dataSet,dictType,dictSize,sampleSize)

dictSize = 1000;
dictType = 'universal';
sampleSize = 100000;

rootDir = '/vol/vssp/diplecs/ash/Data/';
sampleDir = '/collated/';
dictDir = '/Dictionary/';

sampleDataFile = [(rootDir),(dataSet),(sampleDir),(dataSet),num2str(sampleSize),'.uni'];
dictDataFile = [(rootDir),(dataSet),(dictDir),(dataSet),num2str(dictSize),(dictType),num2str(sampleSize),'nmf','beta',num2str(beta),'.dict'];

% load the sample data file
callNMFbeta(sampleDataFile,dictDataFile,dictSize,beta);
fprintf('%s\n',sampleDataFile)

end

function callNMFbeta(sampleDataFile,dictDataFile,dictSize,beta)
    progDir = '/vol/vssp/diplecs/ash/code/nmflib/';
    sampleData = load(sampleDataFile);    
    rndIdx = randsample(size(sampleData,2)-1,4000);
    sampleData = sampleData(:,rndIdx);
    cd (progDir);
    disp('compute dict...');
    tic;
    % W is not normalized
    % H is l1 normalized
    [D,~,~,~] = nmf_beta(sampleData,dictSize,'beta',beta,'niter',10000,'norm_w',0,'norm_h',1,'verb',3);
    toc;
    dlmwrite(dictDataFile,D,'delimiter',',');
    fprintf('%s\n',dictDataFile);
end