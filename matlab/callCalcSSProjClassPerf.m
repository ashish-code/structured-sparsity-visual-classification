function callCalcSSProjClassPerf(dataSet)
colClusts = [5,10,20,30,40,50];
ccTypes = {'i','r'};
dictSize = 1000;

for k = 1 : max(size(ccTypes))
    ccType = ccTypes{k};
    for j = 1 : max(size(colClusts))
        colClust = colClusts(j);
        try
            calcSSProjClassPerf(dataSet,dictSize,colClust,ccType);
        catch err
            fprintf('%s\n',err.identifier);
            fprintf('%d\t%d\t%s\n',dictSize,colClust,ccType);
        end    
    end
end