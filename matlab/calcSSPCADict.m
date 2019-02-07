% compute structured manifold dictionary using sspca and co-clustering
function calcSSPCADict(dataSet,rowClust,colClust,ccType)

dictType = 'universal';
dictSize = 1000;
sampleSize = 100000;
clustAlgo = 'sspca';

rootDir = '/vol/vssp/diplecs/ash/Data/';
sampleDir = '/collated/';
dictDir = '/Dictionary/';
coclustDir = '/CoClust/';

% initialize matlab
cdir = pwd;
cd ~
startup;
cd (cdir)

sampleDataFile = strcat(rootDir,dataSet,sampleDir,dataSet,num2str(sampleSize),'.uni');
dictDataFile = strcat(rootDir,dataSet,dictDir,dataSet,dictType,num2str(dictSize),clustAlgo,num2str(rowClust),num2str(colClust),ccType,'.dict');

if exist(dictDataFile,'file')
    return;
end

% read the cocluster file
% read topic co-cluster file
ccFilePath = strcat(rootDir,dataSet,coclustDir,dataSet,num2str(dictSize),dictType,num2str(sampleSize),ccType,num2str(rowClust),num2str(colClust),'.s');
disp(ccFilePath);
try
    ccfid = fopen(ccFilePath);
    
catch err
    fprintf('%s, %s','unable to open ',ccFilePath);
    fprintf('%s\n',err.identifier);
    return;
end

rowcc = fgetl(ccfid);
fclose(ccfid);

rowcc = textscan(rowcc,'%d ');
rowcc = rowcc{1};
rowcc = rowcc+1;
[ccSort,ccIdx] = sort(rowcc);
ccUnique = unique(ccSort);
nccUnique = max(size(ccUnique));

params.r              = dictSize;
params.it0            = 1;% Cost function displayed every 5 iterations
params.min_delta_cost = 1.0e-12;% Stopping criterion: relative decrease in the cost function smaller than 0.1
params.lambda         = 1.0e-8;
params.normparam      = 1;
params.max_it         = 1000;
params.max_it_U       = 5;
params.max_it_V       = 5;

sampleData = load(sampleDataFile);
sampleData = sampleData';
nVec = size(sampleData,1);
nSample = 10000;
rndSample = randsample(nVec,nSample);
sampleData = sampleData(rndSample,:);

% re-order the dimensions of the data to correpond to the group structure
% provided to SSPCA
sampleData = sampleData(:,ccIdx);

% n = size(sampleData,1);
p = size(sampleData,2);

% group structure
G = zeros(p,nccUnique);

% populate G
for i = 1 : nccUnique
    G(ccSort==i,i) = 1;
end

spG = sparse(G);

% compute dictionary
[ ~, V ] = sspca( sampleData, spG, params );

% U is coefficient matrix n * r
% V is dictionary p * r

dlmwrite(dictDataFile,V,'delimiter',',');
fprintf('%s\n',dictDataFile);

end