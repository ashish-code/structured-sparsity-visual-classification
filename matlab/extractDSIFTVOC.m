% Program to extract dense sift features for images in the dataset VOC2006
% data location: /vol/vssp/diplecs/ash/Data/VOC2006/ImagesPNG/
% descriptors location: /vol/vssp/diplecs/ash/Data/VOC2006/DSIFT/
% file extentions: ####.dsift : imageId + dsift extention 

function extractDSIFTVOC(dataSet)
rootDir = '/vol/vssp/diplecs/ash/Data/';
progPath = '/vol/vssp/diplecs/ash/code/vlfeat-0.9.14/toolbox/';
dataDir = '/TestImagesPNG/';
resultDir = '/TestDSIFT/';
%
binSize = 8;
magnif = 3;
stepSize = 4;

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

 imgDir = strcat(rootDir,dataSet,dataDir);
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
     descFileName = strcat(rootDir,dataSet,resultDir,imageName,'.dsift');
     dlmwrite(descFileName,desc,',');
     disp(descFileName);
 end
 
end