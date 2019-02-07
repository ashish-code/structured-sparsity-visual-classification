'''
Created on 6 Jan 2012

@author: ag00087
'''


#import libraries
from optparse import OptionParser
from sklearn.decomposition import PCA
import numpy as np
import sys

#global parameters
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureMatrix/'
dataExt = '.sift'
dataDim = {'original':128,'lower':3}
outputDir = '/FeatureSubspace/'
catidfname = 'catidlist.txt'

parser = OptionParser()
parser.add_option('-d','--dataset',type='string',metavar='dataset',dest='dataset',default='VOC2006',help='the dataset')
parser.add_option('-l','--lowerDim',type='int',metavar='lowerDim',dest='lowerDim',default=2,help='lower dimension to project data to')

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.loadtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.loadtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

def projectDown():
    (options,args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    lowerDim = options.lowerDim
    
    dataPath = rootDir+dataset+dataDir
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    dataDim['lower']= lowerDim
    for catName in catList:
        print catName       
        dim = dataDim.get('original')
        catFilePath = rootDir+dataset+dataDir+catName+dataExt
        catData = np.genfromtxt(catFilePath,dtype=np.int8,usecols=np.arange(2,dim+2))
        #catImgId = np.genfromtxt(catFilePath,dtype=np.int,usecols=np.arange(dim+2,dim+3))
        catId = np.genfromtxt(catFilePath,dtype=np.int,usecols=np.arange(dim+2,dim+4))
        pca = PCA(n_components=dataDim.get('lower'))
        catDataLower = pca.fit(catData).transform(catData)
        catLower = np.concatenate((catDataLower,catId),axis=1)
        catLowerFilePath = rootDir+dataset+outputDir+catName+'.'+str(dataDim.get('lower'))
        np.savetxt(catLowerFilePath, catLower, fmt='%f', delimiter=' ')
        
if __name__ == '__main__':
    projectDown()
    pass