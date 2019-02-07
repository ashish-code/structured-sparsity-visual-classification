'''
Created on 19 Jan 2012
plot the sspca experiment results
@author: ag00087
'''


import numpy as np
from optparse import OptionParser
import sys


#acquire program arguments
parser = OptionParser()
parser.add_option('-d','--dataset',action='store',type='string',dest='dataset',default='VOC2006',metavar='dataset',help='visual dataset')
parser.add_option('-m','--method',action='store',type='string',dest='method',default='pca',metavar='method',help='the decomposition method to be used {pca, ppca, rpca, kpca, spca')
parser.add_option('-n','--highDim',action='store',type='int',dest='highDim',default=1024,metavar='highDim',help='higher dimensional feature vector')
parser.add_option('-l','--lowDim',action='store',type='int',dest='lowDim',default=128,metavar='lowDim',help='lower dimensional feature vector')
parser.add_option('-q','--quiet',action='store_false',dest='verbose',default=True)

pcaExt = '.pca'
spcaExt = '.spca'
sspcaExt = '.sspca'
kpcaExt = '.kpca'
ppcaExt = '.ppca'
rpcaExt = '.rpca'

higherDims = [512,1024,2048]
lowerDims = [32,64,128,256,512]
methods = ['pca','rpca','kpca','spca','sspca','ppca']

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'


def plotsspcaresult():
    (options, args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    dataset = 'VOC2007'
    
    
    f1scoretable = np.zeros((12,6),np.float)
    count = 0
    for highDim in higherDims:
        for lowDim in lowerDims:
            if (lowDim <= int(highDim/4)):
                try:
                    f1score = np.zeros(6)
                    for i,method in enumerate(methods):
                        fileName = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
                        try:
                            fdata = np.loadtxt(fileName, dtype=np.float, delimiter=' ')
                            f1score[i] = np.mean(fdata)
                        except:
                            #print 'err: %s : %d %d'%(method,highDim,lowDim)
                            pass
                    f1scoretable[count,:] = f1score
                    
                except:
                    pass
                count = count + 1
    print methods
    print f1scoretable
if __name__ == '__main__':
    plotsspcaresult()
    pass
