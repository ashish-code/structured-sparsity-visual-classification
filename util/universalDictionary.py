'''
Created on 16 Feb 2012
compute huge dictionaries for the data
dictionary size: 100,000
@author: ashish@ashishgupta.biz
'''

#libraries
import numpy as np
import sys
from sklearn.cluster import MiniBatchKMeans
from optparse import OptionParser
import time
#parser
parser = OptionParser()
parser.add_option('-d','--dataset',type='string',metavar='dataset',dest='dataset',default='VOC2006',help='the dataset')
parser.add_option('-w','--words',type='int',metavar='words',dest='words',default=1000,help='The dictionary size')
parser.add_option('-s','--samplesize',type='int',metavar='samplesize',dest='samplesize',default=500000,help='The number of sample training feature vectors')
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True)

#path
rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureMatrix/'
iwmDir = '/ImgWrdMat/'
cbDir = '/UniversalCB/'

# global variables
catidfname = 'catidlist.txt'
cbExt = '.ucb'
iwmExt = '.iwm'
dataExt = '.sift'
nDim = 128

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.genfromtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.genfromtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

def computeDictionary():
    (options, args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    words = options.words
    samples = options.samplesize
    #DIAGNOSTIC
    print '%s:%d:%d'%(dataset,words,samples)
    dataPath = rootDir+dataset+dataDir
    #acquire category list
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    #sample <= nCatSample from each visual category
    nCatSample = int(np.round(samples/nCategory));
    print '%s:%d'%('nCatSample',nCatSample)
    count = 0
    #collate sampled data from all the categories
    for catName in catList:
        catFilePath = dataPath+catName+dataExt
        catData = np.loadtxt(catFilePath, dtype= np.int, delimiter=' ', usecols= np.arange(2,nDim+2))
        if(catData.shape[0] < nCatSample):
            catSampleData = catData
        else:
            rndsample = np.random.randint(0,catData.shape[0],nCatSample)
            catSampleData = catData[rndsample,:]
        if(count==0):
            totalSampledData = catSampleData
        else:
            totalSampledData = np.concatenate((totalSampledData,catSampleData),axis=0)
        count+=1
    #CLUSTERING using scikit-learn kmeans
    print '%s:%d'%('sampleSize',totalSampledData.shape[0])
    mbk = MiniBatchKMeans(init='k-means++', k=words, max_iter=5, batch_size=int(np.round(samples/100)),
                  n_init=samples/1000, max_no_improvement=int(np.round(0.01*samples)), verbose=0)
    t0 = time.time()
    mbk.fit(totalSampledData)
    t_mini_batch = time.time() - t0
    #DIAGNOSTIC
    print '%:%s:%s:%d'%('Time',dataset,catName,t_mini_batch)
    mbk_cluster_centers = mbk.cluster_centers_
    # write dictionary to file
    cbfilepath = rootDir+dataset+cbDir+dataset+str(words)+'_'+str(nDim)+cbExt
    cbfile = open(cbfilepath,'w')
    np.savetxt(cbfile,mbk_cluster_centers,fmt='%f', delimiter=' ')
    cbfile.close()
   
    pass

if __name__ == '__main__':
    computeDictionary()
    pass