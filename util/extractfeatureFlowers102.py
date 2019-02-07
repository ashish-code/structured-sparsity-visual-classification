'''
Created on 25 Nov 2011

@author: ag00087
'''
#global imports
import os
import numpy as np

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/ImagesPNG/'
dataSet = 'Flowers102'
progDir = '/vol/vssp/diplecs/ash/code/descriptorvgg/'
prog = 'extract_features.ln'
featureDir = '/Feature/'
catListFile = 'categoryList.txt'
descext = '.sift'
paramext = '.params'
imageLabelFileName = 'imagelabels.txt'

def readCategoryList(dataSet):
    catListFilePath = rootDir+dataSet+'/'+catListFile
    catList = np.loadtxt(catListFilePath,dtype='|S32')
    return catList

def extractFlowers102():
    catList = readCategoryList(dataSet)
    imageLabelFilePath = rootDir+dataSet+'/'+imageLabelFileName
    imageLabel = np.loadtxt(imageLabelFilePath,dtype=np.int,delimiter=',')
    for iCategory,categoryName in enumerate(catList):
        catImageIds = np.nonzero(imageLabel==iCategory+1)
        catImageIds = [id for id in catImageIds[0]]
        catDirPath = rootDir+dataSet+featureDir+categoryName
        if not os.path.exists(catDirPath):
            os.mkdir(catDirPath)
        for catImageId in catImageIds:
            catImageName = rootDir+dataSet+dataDir+'image_%05d.png'%(catImageId)
            featureFileName = rootDir+dataSet+featureDir+categoryName+'/'+'%05d.sift'%(catImageId)
            paramFileName = rootDir+dataSet+featureDir+categoryName+'/'+'%05d.sift.params'%(catImageId)
            oldparamFileName = rootDir+dataSet+featureDir+categoryName+'/'+'%05d.params'%(catImageId)
            
            print catImageName
            print featureFileName
            com = progDir+prog+' -harlap -sift'+' -i '+catImageName+' -o1 '+featureFileName
            os.system(com)
            commanddel = 'rm '+ paramFileName
            if os.path.exists(paramFileName):
                os.system(commanddel)
            commanddel = 'rm '+ oldparamFileName
            if os.path.exists(oldparamFileName):
                os.system(commanddel)
            pass
        pass

if __name__=='__main__':
    extractFlowers102()
    pass