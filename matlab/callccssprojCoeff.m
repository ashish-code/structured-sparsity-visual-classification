function callccssprojCoeff(dataSet,ccType,dictSize)

colClusts = [5,10,20,30,40,50];

for j = 1 : max(size(colClusts))
    colClust = colClusts(j);
    try
        ccssprojcoeff(dataSet,dictSize,colClust,ccType);
    catch err
        fprintf('%s\n',err.identifier);
        fprintf('%d\t%d\t%s\n',dictSize,colClust,ccType);
    end    
end
end