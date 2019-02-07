'''
Created on 19 Jan 2012
plot comparative performance of sspca for various categories of a dataset
@author: ag00087
'''


import numpy as np
from optparse import OptionParser
import sys
import matplotlib.pyplot as plt


spcaExt = '.spca'
sspcaExt = '.sspca'

higherDims = [512,1024,2048]
lowerDims = [32,64,128,256,512]
methods = ['spca','sspca']
datasets = ['VOC2006','VOC2007','VOC2010','Scene15','Birds','Butterflies']

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'
catidfname = 'catidlist.txt' # list of categories in the dataset

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.genfromtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.genfromtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap
def plotsspcaresult():
    dataset = 'VOC2006'
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
        
    f1Avgscoretable = np.zeros((nCategory,len(methods)),np.float)
   
    highDim = 1024
    lowDim = 128
        
    
        
    for i,method in enumerate(methods):
        fileNameAvg = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
        try:
            fdataAvg = np.loadtxt(fileNameAvg, dtype=np.float, delimiter=' ')
            f1Avgscoretable[:,i] = fdataAvg                 
        except:
            print 'err: %s : %d %d'%(method,highDim,lowDim)
            pass
    
    
    outPath = resultRootDir+'results'+'/'+dataset+'categories'+str(highDim)+str(lowDim)+'.png'
    
    fig = plt.figure()
    figfmt = 'png'
    ax = fig.add_subplot(111)
    plt.plot(np.arange(nCategory),f1Avgscoretable[:,0],'b--o',linewidth=2.5,label='SPCA')
    plt.plot(np.arange(nCategory),f1Avgscoretable[:,1],'k-s',linewidth=2.5,label='SSPCA')
    plt.xlabel('Data sets',size='large')
    plt.ylabel('F1_score',size='large')
    plt.title('%s: %s->%s ' %(dataset,str(highDim),str(lowDim)) ,size='large')
    plt.legend(loc="upper right")
    maxf1 = np.max(f1Avgscoretable)+0.04*np.mean(f1Avgscoretable)
    minf1 = np.min(f1Avgscoretable)-0.04*np.mean(f1Avgscoretable)
    plt.ylim([minf1,maxf1])
    
    ax.set_xticks(np.arange(len(datasets)))
    ax.set_xticklabels(datasets,rotation=0,size='medium',ha='center')
    #plt.savefig(outPath,format=figfmt)
    plt.show()
    plt.close()
    
def plotsspcaBar():
    
    pass
if __name__=='__main__':
    plotsspcaresult()
