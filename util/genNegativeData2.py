'''
Created on 7 Jan 2012
Generate negative data for binary classifier
The first and primary use of this data is by the fuzzy encoding paper
@author: a.gupta@surrey.ac.uk
'''


#import libraries
from optparse import OptionParser
import numpy as np
import sys
import random
import os

#global parameters
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureMatrix/'

dataDim = {'original':128,'lower':3}
outputDir = '/FeatureMatrix/'
catidfname = 'catidlist.txt'
dataExt = '.sift'
parser = OptionParser()
parser.add_option('-d','--dataset',type='string',metavar='dataset',dest='dataset',default='VOC2006',help='the dataset')
parser.add_option('-l','--lowerDim',type='int',metavar='lowerDim',dest='lowerDim',default=128,help='lower dimension to project data to')

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.loadtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.loadtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

def genNegativeData():
    (options,args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    
#    dataExt = '.'+str(dataDim.get('lower'))
    dim = dataDim['original']
    for catName in (catList):
        print catName
        catNegFilePath = rootDir+dataset+outputDir+'NEG'+catName+dataExt
        if os.path.exists(catNegFilePath):
            print '%s'%(catNegFilePath)
            continue
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
                imgidsample = random.sample(imgids,nSampleImagePerCategory)
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
            #catNegFilePath = rootDir+dataset+outputDir+'NEG'+catName+dataExt
            print 'writing %s'%(catNegFilePath)
            np.savetxt(catNegFilePath, catNegData, fmt='%f', delimiter=' ')
        pass
    pass

if __name__=='__main__':
    genNegativeData()
    pass