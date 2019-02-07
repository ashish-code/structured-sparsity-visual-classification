'''
Created on 29 Nov 2011
Write the features extracted in Feature to FeatureMatrix
It is a matrix of the all the descriptors collated from one category
The format of each descriptor is:
X Y <128-descriptor> ImgId CategoryId
@author: ag00087
'''

#global imports
import numpy as np
import os
import csv
import sys

#global parameters
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataSets = ['Birds','Butterflies','Flowers17','Flowers102','UIUC']
featureDir = '/Feature/'
featureMatrixDir = '/FeatureMatrix/'
categoryListFileName = 'categoryList.txt'
categoryIdFileName = 'catidlist.txt'
#file extensions
descext = '.sift'

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-d','--dataset',action='store',type='string',dest='dataset',metavar='dataset',default='UIUC',help='visual dataset')

def getCatMap(dataSet):
    catidfpath = rootDir+dataSet+'/'+categoryIdFileName
    catnames = np.genfromtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.genfromtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap

def readCategoryList(dataSet):
    '''
    Reads the category list file and returns list of category names.
    The directory names are the same as the category name.
    '''
    catListFilePath = rootDir+dataSet+'/'+categoryListFileName
    catList = np.loadtxt(catListFilePath,dtype='|S32')
    return catList

def writeFeatureMatrix():
    '''
    collate descriptors of each category in the data set
    '''
    (options, args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataSet = options.dataset
    catMap = getCatMap(dataSet)
    catList = catMap.keys()
#    catList = readCategoryList(dataSet)
    for categoryName in catList:
        categoryPath = rootDir+dataSet+featureDir+categoryName
        imgFileList = os.listdir(categoryPath)
        # there may be other types of files in the directory so filter them out
        imgFileList = [i for i in imgFileList if i.endswith('.sift')]
        
        # file to write the feature vector to        
        featureMatrixFileName = rootDir+dataSet+featureMatrixDir+categoryName+descext
        if os.path.exists(featureMatrixFileName):
            os.remove(featureMatrixFileName)
        featureMatrixFile = csv.writer(open(featureMatrixFileName,'a'),delimiter=' ')
        
        # collate features for each image
        for img in imgFileList:
            # check if the file is a sift descriptor file
            if(img.endswith('sift')):
                imgFileName = rootDir+dataSet+featureDir+categoryName+'/'+img
                if not os.path.getsize(imgFileName) == 0:
                    imgData = np.loadtxt(imgFileName,delimiter=' ',dtype=np.int,skiprows=2,usecols=np.concatenate((np.arange(0,2),np.arange(5,133))))
                    nvectors = imgData.shape[0]
                    catidarr = int(catMap.get(categoryName))*np.ones(nvectors,dtype=np.int)
                    imgId = int(img.split('.')[0])
                    imgidarr = imgId*np.ones(nvectors,dtype=np.int)
                    featureMatrixData = np.vstack((imgData.T,imgidarr,catidarr)).T
                    featureMatrixFile.writerows(featureMatrixData)
                    print '%s:%s:%s'%(dataSet,categoryName,img)
                    pass
            pass
        print '%s'%(featureMatrixFileName)
        pass
    pass

if __name__ == '__main__':
    writeFeatureMatrix()
    pass