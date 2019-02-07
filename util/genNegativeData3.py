'''
Created on 9 Jan 2012
Generate negative training samples.
Errata: (1) Check for sample size
(2) skip category if file already present
@author: ag00087
'''

#import libraries
from optparse import OptionParser
import numpy as np
import sys
import random
import os

#global parameters
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureSubspace/'

dataDim = {'lower':3}
outputDir = '/FeatureSubspace/'
catidfname = 'catidlist.txt'

parser = OptionParser()
parser.add_option('-d','--dataset',type='string',metavar='dataset',dest='dataset',default='VOC2006',help='the dataset')
parser.add_option('-l','--lowerDim',type='int',metavar='lowerDim',dest='lowerDim',default=12,help='lower dimension to project data to')

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.loadtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.loadtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

def genNegativeData():
    (options,args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    lowerDim = options.lowerDim
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    dataDim['lower']= lowerDim
    dataExt = '.'+str(dataDim.get('lower'))
    for catName in (catList):
        catNegFilePath = rootDir+dataset+outputDir+'NEG'+catName+dataExt
        if os.path.exists(catNegFilePath):
            print '%s'%catNegFilePath 
            continue
        print catName
        dim = dataDim.get('lower')
        catFilePath = rootDir+dataset+dataDir+catName+dataExt
        #catData = np.genfromtxt(catFilePath,dtype=np.float,usecols=np.arange(0,dim))
        catImgId = np.genfromtxt(catFilePath,dtype=np.int,usecols=np.arange(dim,dim+1))
        #catId = np.genfromtxt(catFilePath,dtype=np.int,usecols=np.arange(dim+1,dim+2))
        nImage = np.unique(catImgId).shape[0]
        print 'nImage: %d'%(nImage)
        nSampleImagePerCategory = np.round(nImage/(nCategory-1))
        #at least one image is selected from the dataset
        if nSampleImagePerCategory < 1:
            nSampleImagePerCategory = 1
        print 'nSampleImagePerCategory: %d'%(nSampleImagePerCategory)
        count = 0
        createSwitch = True
        for nameCat in (catList):
            if nameCat != catName:
                print nameCat
                catFilePath = rootDir+dataset+dataDir+nameCat+dataExt
                catData = np.genfromtxt(catFilePath,dtype=np.float)
                catImgId = np.genfromtxt(catFilePath,dtype=np.int,usecols=np.arange(dim,dim+1))
                imgids = np.unique(catImgId)
                if (imgids.shape[0] > nSampleImagePerCategory):
                    imgidsample = random.sample(imgids,nSampleImagePerCategory)
                else:
                    imgidsample = imgids
                
                for imgid in imgidsample:
                    ids = np.where(catImgId==imgid)[0] 
                    catSampleData = catData[ids,:]
                    count = count + 1
                    catSampleData[:,dim]=count
                    catSampleData[:,dim+1]=-1
                    if createSwitch:
                        createSwitch = False
                        catNegData = catSampleData
                    else:
                        catNegData = np.concatenate((catNegData,catSampleData),axis=0)
                pass
            pass
        # write the category negative to file
        
        print 'writing %s'%(catNegFilePath)
        np.savetxt(catNegFilePath, catNegData, fmt='%f', delimiter=' ')
        pass
    pass

if __name__=='__main__':
    genNegativeData()
    pass