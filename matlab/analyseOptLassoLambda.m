% analyse the classification performance for different dictionaries and
% sparse decomposition schemes
% report on appropriate values for further tuning

function analyseOptLassoLambda(dataSet)
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

sparseDecomp = 'Lasso';

modes = [0,1,2];
modeDs = [0];
modeLs = [0,1,2];
nModes = max(size(modes));
nModeDs = max(size(modeDs));
nModeLs = max(size(modeLs));

for iMode = 1 : nModes
    for iModeD = 1 : nModeDs
        for iModeL = 1 : nModeLs
            % grid search value of lambda based on dictionary learning mode
            mode = modes(iMode);
            modeD = modeDs(iModeD);
            modeL = modeLs(iModeL);
            lambdas = [1,10,100,500,1000,5000,10000];
            nLambda = max(size(lambdas));
            perfAP = zeros(nLambda,3);
            perfAPFileName = [(rootDir),(dataSet),(lambdaPerfDir),'mode',num2str(mode),'modeD',num2str(modeD),'modeL',num2str(modeL),(sparseDecomp),'.avg'];
            for iLambda = 1 : nLambda
                lambda = lambdas(iLambda);
                lambdaPerFileAvg = [(rootDir),(dataSet),(lambdaDir),'mode',num2str(mode),'modeD',num2str(modeD),'lambda',num2str(lambda),'modeL',num2str(modeL),(sparseDecomp),'.avg'];
                try
                    perf = dlmread(lambdaPerFileAvg,',');
                    perfAPAvg = mean(perf(:,1));
                    perfAPStd = std(perf(:,1));
                    fprintf('%d\t%d\t%d\t%f\t%f\t%f\n',mode,modeD,modeL,lambda,perfAPAvg,perfAPStd);
                    perfAP(iLambda,1) = lambda;
                    perfAP(iLambda,2) = perfAPAvg;
                    perfAP(iLambda,3) = perfAPStd;
                catch err
                    disp(err.identifier);
                end
                
            end
        end
        dlmwrite(perfAPFileName,perfAP,'delimiter',',');
    end
end


end