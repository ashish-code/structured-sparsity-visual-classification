% function to call calcSSPCAClassPerf(dataSet,ccType,rowClust,colClust,method)
function callcalcSSPCAClassPerf(rowClust,colClust)

methods = {'VQ'};
nMethods = max(size(methods));
dataSets = {'VOC2006', 'VOC2007', 'VOC2010', 'Scene15'};
nDataSets = max(size(dataSets));
ccTypes = {'i','e','r'};
nCcTypes = max(size(ccTypes));

for i = 1 : nDataSets
    dataSet = dataSets{i};
    for j = 1 : nCcTypes
        ccType = ccTypes{j};
        for k = 1 : nMethods
            method = methods{k};
            try
                calcSSPCAClassPerf(dataSet,ccType,rowClust,colClust,method);
            catch err
                fprintf('%s\n',err.identifier);
                fprintf('%s,%s,%s',dataSet,ccType,method);
            end
        end
    end
end

end