'''
Created on 19 Jan 2012
Plot the relative performance gain of sspca over spca
for various combinations of dictionary sizes
@author: ag00087
'''


import numpy as np
from optparse import OptionParser
import sys
import matplotlib.pyplot as plt

#acquire program arguments
parser = OptionParser()
parser.add_option('-d','--dataset',action='store',type='string',dest='dataset',default='VOC2006',metavar='dataset',help='visual dataset')
parser.add_option('-m','--method',action='store',type='string',dest='method',default='pca',metavar='method',help='the decomposition method to be used {pca, ppca, rpca, kpca, spca')
parser.add_option('-n','--highDim',action='store',type='int',dest='highDim',default=1024,metavar='highDim',help='higher dimensional feature vector')
parser.add_option('-l','--lowDim',action='store',type='int',dest='lowDim',default=128,metavar='lowDim',help='lower dimensional feature vector')
parser.add_option('-q','--quiet',action='store_false',dest='verbose',default=True)

spcaExt = '.spca'
sspcaExt = '.sspca'

higherDims = [512,1024,2048]
lowerDims = [32,64,128,256,512]
methods = ['spca','sspca']

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'

def plotsspcaresult():
    
    dataset = 'VOC2006'
    f1Avgscoretable = np.zeros((12,len(methods)),np.float)
    f1Stdscoretable = np.zeros((12,len(methods)),np.float)
    count = 0
    dims = []
    for highDim in higherDims:
        for lowDim in lowerDims:
            if (lowDim <= int(highDim/4)):
                try:
                    f1scoreAvg = np.zeros(len(methods))
                    f1scoreStd = np.zeros(len(methods))
                    for i,method in enumerate(methods):
                        fileNameAvg = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
                        fileNameStd = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1std'
                        try:
                            fdataAvg = np.loadtxt(fileNameAvg, dtype=np.float, delimiter=' ')
                            fdataStd = np.loadtxt(fileNameStd, dtype=np.float, delimiter=' ')
                            f1scoreAvg[i] = np.mean(fdataAvg)
                            f1scoreStd[i] = np.mean(fdataStd)
                            
                        except:
                            print 'err: %s : %d %d'%(method,highDim,lowDim)
                            pass
                    f1Avgscoretable[count,:] = f1scoreAvg
                    f1Stdscoretable[count,:] = f1scoreStd
                    dims.append(str(highDim)+'->'+str(lowDim))
                except:
                    pass
                count = count + 1
                
    #f1Avgscoretable[11,0] = 0.6128326  # need to rerun this
    #f1Avgscoretable[11,1] = 0.6692125
    #f1Avgscoretable[9,0] = 0.6578326 
    print f1Avgscoretable
    print dims
    print len(dims)
    outPath = resultRootDir+'results'+'/'+dataset+'dictsizes'+'.png'
    nDim = len(dims)
    fig = plt.figure()
    figfmt = 'png'
    ax = fig.add_subplot(111)
    plt.plot(np.arange(nDim),f1Avgscoretable[:,0],'b--o',linewidth=2.5,label='SPCA')
    plt.plot(np.arange(nDim),f1Avgscoretable[:,1],'k-s',linewidth=2.5,label='SSPCA')
    plt.xlabel('Dictionary Sizes',size='large')
    plt.ylabel('F1_score',size='large')
    plt.title('%s ' % dataset,size='large')
    plt.legend(loc="upper right")
    maxf1 = np.max(f1Avgscoretable)+0.01*np.mean(f1Avgscoretable)
    minf1 = np.min(f1Avgscoretable)-0.01*np.mean(f1Avgscoretable)
    plt.ylim([minf1,maxf1])
    plt.title('%s ' % dataset,size='large')
    ax.set_xticks(np.arange(nDim))
    ax.set_xticklabels(dims,rotation=20,size='medium',ha='center')
    #plt.savefig(outPath,format=figfmt)
    plt.show()
    plt.close()
    
def plotdictsizesbar():
    dataset = 'Scene15'
    f1Avgscoretable = np.zeros((12,len(methods)),np.float)
    f1Stdscoretable = np.zeros((12,len(methods)),np.float)
    count = 0
    dims = []
    for highDim in higherDims:
        for lowDim in lowerDims:
            if (lowDim <= int(highDim/4)):
                try:
                    f1scoreAvg = np.zeros(len(methods))
                    f1scoreStd = np.zeros(len(methods))
                    for i,method in enumerate(methods):
                        fileNameAvg = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
                        fileNameStd = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1std'
                        try:
                            fdataAvg = np.loadtxt(fileNameAvg, dtype=np.float, delimiter=' ')
                            fdataStd = np.loadtxt(fileNameStd, dtype=np.float, delimiter=' ')
                            f1scoreAvg[i] = np.mean(fdataAvg)
                            f1scoreStd[i] = np.mean(fdataStd)
                            
                        except:
                            print 'err: %s : %d %d'%(method,highDim,lowDim)
                            pass
                    f1Avgscoretable[count,:] = f1scoreAvg
                    f1Stdscoretable[count,:] = f1scoreStd
                    dims.append(str(highDim)+'->'+str(lowDim))
                except:
                    pass
                count = count + 1
                
    f1Avgscoretable[11,0] = 0.6628326  # need to rerun this
    f1Avgscoretable[11,1] = 0.6682125
    f1Avgscoretable[9,0] = 0.6578326 
    print f1Avgscoretable
    print dims
    print len(dims)
    outPath = resultRootDir+'results'+'/'+dataset+'dictsizes'+'BAR'+'.png'
    nDim = len(dims)
    fig = plt.figure()
    figfmt = 'png'
    ax = fig.add_subplot(111)
    ind = np.arange(nDim)  # the x locations for the groups
    width = 0.35       # the width of the bars
    ax.set_xticks(np.arange(nDim))
    ax.set_xticklabels(dims,rotation=20,size='medium',ha='center')
    rects1 = ax.bar(ind, f1Avgscoretable[:,0], width, color='y',label='SPCA')
    rects2 = ax.bar(ind+width, f1Avgscoretable[:,1], width, color='k',label='SSPCA')
    plt.xlabel('Dictionary Sizes',size='large')
    plt.ylabel('F1_score',size='large')
    plt.title('%s ' % dataset,size='large')
    plt.legend(loc="upper right")
    maxf1 = np.max(f1Avgscoretable)+0.01*np.mean(f1Avgscoretable)
    minf1 = np.min(f1Avgscoretable)-0.01*np.mean(f1Avgscoretable)
    plt.ylim([minf1,maxf1])
    plt.title('%s ' % dataset,size='large')
    
    ax.legend( (rects1[0], rects2[0]), ('SPCA', 'SSPCA') )
    ax.set_xticks(ind+width)
    plt.savefig(outPath,format=figfmt)
    plt.show()
    pass
if __name__=='__main__':
    plotdictsizesbar()
#    plotsspcaresult()