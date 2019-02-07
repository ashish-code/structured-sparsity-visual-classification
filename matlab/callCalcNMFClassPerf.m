% call classification perf for nmf alpha and nmf beta coefficients
function callCalcNMFClassPerf(algo)

dictType = 'universal';
dictSize = 1000;
method = 'Lasso';
sampleSize = 100000;

if strcmp(algo,'nmfbeta')
    paramlist = [1, 2];
elseif strcmp(algo,'nmfalpha')
    paramlist = [-1, 0.5, 2];
else
    return;
end

nParamList = max(size(paramlist));
dataSets = {'VOC2006', 'VOC2007', 'VOC2010', 'Scene15', 'Caltech101'};
nDataSets = max(size(dataSets));

for iDataSet = 1 : nDataSets
    dataSet = dataSets{iDataSet};
    for iParam = 1 : nParamList
        param = paramlist(iParam);
        try
            calcClassificationPerf(dataSet,dictType,dictSize,sampleSize,algo,param,method);
        catch err
            fprintf('%s\n',err.identifier);
        end
    end
end

end