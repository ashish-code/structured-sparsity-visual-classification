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
dataSet = 'Birds'
progDir = '/vol/vssp/diplecs/ash/code/descriptorvgg/'
prog = 'extract_features.ln'
featureDir = '/Feature/'
catListFile = 'categoryList.txt'
descext = '.sift'
paramext = '.params'

def readCategoryList(dataSet):
    catListFilePath = rootDir+dataSet+'/'+catListFile
    catList = np.loadtxt(catListFilePath,dtype='|S32')
    return catList

def extractBirds():
       
    catlist = readCategoryList(dataSet)
    
    for catName in catlist:
        dataPath = rootDir+dataSet+dataDir+catName+'/'
        imageList = os.listdir(dataPath)
        
        featurePath = rootDir+dataSet+featureDir+catName+'/'
        if not os.path.isdir(featurePath):
            os.mkdir(featurePath)
        
        for img in imageList:
            if(img.split('.')[1]=='png'):
                imgName = img.split('.')[0][3:] 
                featureFileName = featurePath+imgName+descext
                imgFileName = dataPath+img
                com = progDir+prog+' -harlap -sift'+' -i '+imgFileName+' -o1 '+featureFileName
                os.system(com)
                print 'featureVector: %s'%(featureFileName)
                paramFileName = featurePath+imgName+paramext
                commanddel = 'rm '+ paramFileName
                if os.path.exists(paramFileName):
                    os.system(commanddel)

if __name__ == '__main__':
    extractBirds()
    pass