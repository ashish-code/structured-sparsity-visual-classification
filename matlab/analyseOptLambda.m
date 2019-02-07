% analyse the classification performance for different dictionaries and
% sparse decomposition schemes
% report on appropriate values for further tuning

function analyseOptLambda(dataSet)
% function analyseOptLambda(dataSet,dictType,dictSize,sampleSize)
% dataSet = 'VOC2006'
% dictType = 'universal'
% dictSize = 1000;
% sampleSize = 100000;

rootDir = '/vol/vssp/diplecs/ash/Data/';
lambdaDir = '/lambda/';
lambdaPerfDir = '/lambdaPerf/';

% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);



modes = [0,1,2,3,4,5];
modeDs = [0,1,2];
nModes = max(size(modes));
nModeDs = max(size(modeDs));


for iMode = 1 : nModes
    for iModeD = 1 : nModeDs
        % grid search value of lambda based on dictionary learning mode
        mode = modes(iMode);
        modeD = modeDs(iModeD);
        if ismember(mode,[0,1,2,4,5])
            lambdas = power(10,-3:1:4);
        elseif mode == 3
            lambdas = 0.2:0.1:0.9;
        end
        nLambda = max(size(lambdas));
        perfAP = zeros(nLambda,3);
        perfAPFileName = [(rootDir),(dataSet),(lambdaPerfDir),'mode',num2str(mode),'modeD',num2str(modeD),'.avg'];
        for iLambda = 1 : nLambda
            lambda = lambdas(iLambda);
            lambdaPerFileAvg = [(rootDir),(dataSet),(lambdaDir),'mode',num2str(mode),'modeD',num2str(modeD),'lambda',num2str(lambda),'.avg'];
            try
                perf = dlmread(lambdaPerFileAvg,',');
            catch err
                disp(err.identifier);
            end
            perfAPAvg = mean(perf(:,1));
            perfAPStd = std(perf(:,1));
            fprintf('%d\t%d\t%f\t%f\t%f\n',mode,modeD,lambda,perfAPAvg,perfAPStd);
            perfAP(iLambda,1) = lambda;
            perfAP(iLambda,2) = perfAPAvg;
            perfAP(iLambda,3) = perfAPStd;
        end
        dlmwrite(perfAPFileName,perfAP,'delimiter',',');
    end
end


end