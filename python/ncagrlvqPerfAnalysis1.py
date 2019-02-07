'''
Created on 10 Apr 2012
analyse performance of the ncagrlvq experiments
The four methods used are:
pcakmeans
pcagrlvq
ncakmeans
ncagrlvq
@author: ag00087
'''


import numpy as np
import sys
from optparse import OptionParser
import matplotlib.pyplot as plt

rootDir = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/NCAGRLVQ/'

parser = OptionParser()
parser.add_option('-d','--dataset',type='string',metavar='dataset',dest='dataset',default='VOC2006',help='the dataset')
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True)
parser.add_option('-w','--nWord',type='int',metavar='nWord',dest='nWord',default=400,help='codewords')
parser.add_option("-s",'--nDim',type='int',metavar='nDim',dest='nDim',default=3,help='dimensionality of sub-space')
parser.add_option('-p','--figformat',type='string',metavar='figfmt',dest='figfmt',default='png',help='type of output graph image, png, svg, jpg')

methods = ['pcakmeans','pcagrlvq','ncakmeans','ncagrlvq']
accExt = '.acc'
f1Ext = '.f1'

def plotncagrlvq(dataset,nWord,nDim):
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    nMethod = len(methods)
    result = np.zeros((nMethod,nCategory),np.double)
    for iMethod,method in enumerate(methods):
        resultDir = rootDir+dataset+dataDir+method+'/'
        resultFile = resultDir+'yin_yang'+str(nWord)+str(nDim)+f1Ext
        try:
            result[iMethod,:] = np.loadtxt(resultFile,dtype=np.double,delimiter=' ')
        except:
            print 'err: '+resultFile
        pass
    print result
    avgResult = np.mean(result,1)
    print avgResult
    # plot the results
    
    pass

def getCatMap(dataset):
    catidfname = 'catidlist.txt'
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.genfromtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.genfromtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap    

if __name__ == '__main__':
    dataset = 'Caltech101'
    nWord = 1000
    nDim = 12
    plotncagrlvq(dataset,nWord,nDim)
    pass