% Program to extract dense sift features for images in the dataset VOC2006
% data location: /vol/vssp/diplecs/ash/Data/VOC2006/ImagesPNG/
% descriptors location: /vol/vssp/diplecs/ash/Data/VOC2006/DSIFT/
% file extentions: ####.dsift : imageId + dsift extention 

function extractDSIFTOther(dataSet)
rootDir = '/vol/vssp/diplecs/ash/Data/';
dataDir = '/ImagesPNG/';
if strcmp(dataSet,'')
    dataSet = 'Scene15';
end
categoryListFileName = 'categoryList.txt';
progPath = '/vol/vssp/diplecs/ash/code/vlfeat-0.9.14/toolbox/';
resultDir = '/DSIFT/';
%
binSize = 8;
magnif = 3;
stepSize = 4;
% -------------------------------------------------------------------
% read the category list in the dataset
% -------------------------------------------------------------------
categoryListPath = [(rootDir),(dataSet),'/',(categoryListFileName)];
fid = fopen(categoryListPath);
categoryList = textscan(fid,'%s');
categoryList = categoryList{1};
fclose(fid);
% number of categories in list
nCategory = size(categoryList,1);
%
% -------------------------------------------------------------------
% Initialize paths in matlab
% -------------------------------------------------------------------
 cdir = pwd;
 cd ~;
 startup;
 cd (progPath)
 vl_setup;
 cd (cdir);
 %
 for j = 1 : nCategory
     catName = categoryList{j};
     
     imgDir = [rootDir dataSet dataDir catName '/'];
     cd (imgDir);
     imageList = dir('.');
     nFile = size(imageList);
     for i = 3:nFile
         imageFileName = imageList(i).name;
         dospos = strfind(imageFileName,'.');
         imageName = imageFileName(1:dospos-1);
         imagePath = [imgDir imageFileName];
         img = imread(imagePath);
         if ndims(img) == 3
             img = rgb2gray(img);
         end
         img = single(vl_imdown(img));
         imgSmooth = vl_imsmooth(img, sqrt((binSize/magnif)^2 - .25)) ;
         [f, d] = vl_dsift(imgSmooth, 'size', binSize, 'step', stepSize);
         desc = [f;d];
         disp(size(desc,1))
         descFileDir = [rootDir dataSet resultDir catName '/'];
         if ~exist(descFileDir,'dir')
            mkdir(descFileDir)
         end
         descFileName = [descFileDir imageName '.dsift'];
         dlmwrite(descFileName,desc,',');
         disp(descFileName);
     end
 end
end