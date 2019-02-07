% collate sspca class performance

function collateSSPCAClassPerf(rowClust,colClust,ccType,method)

% initialize matlab
cdir = pwd;
cd ~;
startup;
cd (cdir);

dataSets = {'VOC2006', 'VOC2007'};
nDataSets = max(size(dataSets));
rootDir = '/vol/vssp/diplecs/ash/Data/';
resultDir = 'Result/';
coeffPerfDir = '/CoeffPerf/';
algo = 'sspca';
param = '';

resultFile = strcat(rootDir,resultDir,'sspca',num2str(rowClust),num2str(colClust),ccType,method,'.csv');
resultfid = fopen(resultFile,'w');
fprintf(resultfid,'%s,%s,%s\n','DataSet','Category','mAP');

for i = 1 : nDataSets
    dataSet = dataSets{i};
    coeffPerfFileAvg  = strcat(rootDir,dataSet,coeffPerfDir,algo,num2str(param),method,num2str(rowClust),num2str(colClust),ccType,'.avg');
    coeffPerf = dlmread(coeffPerfFileAvg,',');
    categoryListFileName = 'categoryList.txt';
    categoryListPath = strcat(rootDir,dataSet,'/',categoryListFileName);
    fid = fopen(categoryListPath);
    categoryList = textscan(fid,'%s');
    categoryList = categoryList{1};
    fclose(fid);
    nCategory = size(categoryList,1);
    for iCategory = 1 : nCategory
        category = categoryList{iCategory};
        map = coeffPerf(iCategory,1);
        fprintf(resultfid,'%s,%s,%f\n',dataSet,category,map);
        fprintf('%s,%s,%f\n',dataSet,category,map);
    end
end
fclose(resultfid);
fprintf('%s\n',resultFile);

end