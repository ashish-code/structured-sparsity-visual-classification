'''
Created on 4 Jan 2012
Read feature descriptor data for each category of given dataset
and write the feature vector for balanced data
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


def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.loadtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.loadtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

def projectDown():
    (options,args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    
    dataPath = rootDir+dataset+dataDir
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    
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