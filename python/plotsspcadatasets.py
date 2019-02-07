'''
Created on 19 Jan 2012
plot comparative sspca performance for various datasets
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
datasets = ['VOC2006','VOC2007','VOC2010','Scene15']

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'

def plotsspcaresult():
    
    
    f1Avgscoretable = np.zeros((len(datasets),len(methods)),np.float)
   
    highDim = 2048
    lowDim = 32
    nDataset = len(datasets)
    for idataset,dataset in enumerate(datasets):
        try:
            f1scoreAvg = np.zeros(len(methods))
            for i,method in enumerate(methods):
                fileNameAvg = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
                try:
                    fdataAvg = np.loadtxt(fileNameAvg, dtype=np.float, delimiter=' ')
                    f1scoreAvg[i] = np.mean(fdataAvg)                    
                except:
                    print 'err: %s : %d %d'%(method,highDim,lowDim)
                    pass
            f1Avgscoretable[idataset,:] = f1scoreAvg
        except:
            pass
    
    outPath = resultRootDir+'results'+'/'+'datasets'+str(highDim)+str(lowDim)+'.png'
    
    fig = plt.figure()
    figfmt = 'png'
    ax = fig.add_subplot(111)
    plt.plot(np.arange(nDataset),f1Avgscoretable[:,0],'b--o',linewidth=2.5,label='SPCA')
    plt.plot(np.arange(nDataset),f1Avgscoretable[:,1],'k-s',linewidth=2.5,label='SSPCA')
    plt.xlabel('Data sets',size='large')
    plt.ylabel('F1_score',size='large')
    plt.title('%s->%s ' %(str(highDim),str(lowDim)) ,size='large')
    plt.legend(loc="upper right")
    maxf1 = np.max(f1Avgscoretable)+0.04*np.mean(f1Avgscoretable)
    minf1 = np.min(f1Avgscoretable)-0.04*np.mean(f1Avgscoretable)
    plt.ylim([minf1,maxf1])
    
    ax.set_xticks(np.arange(len(datasets)))
    ax.set_xticklabels(datasets,rotation=0,size='medium',ha='center')
    plt.savefig(outPath,format=figfmt)
    plt.show()
    plt.close()
    
def plotsspcaDatasetBar():
    f1Avgscoretable = np.zeros((len(datasets),len(methods)),np.float)
   
    highDim = 2048
    lowDim = 128
    nDataset = len(datasets)
    for idataset,dataset in enumerate(datasets):
        try:
            f1scoreAvg = np.zeros(len(methods))
            for i,method in enumerate(methods):
                fileNameAvg = resultRootDir+dataset+'/'+str(highDim)+str(lowDim)+method+'.f1avg'
                try:
                    fdataAvg = np.loadtxt(fileNameAvg, dtype=np.float, delimiter=' ')
                    f1scoreAvg[i] = np.mean(fdataAvg)                    
                except:
                    print 'err: %s : %d %d'%(method,highDim,lowDim)
                    pass
            f1Avgscoretable[idataset,:] = f1scoreAvg
        except:
            pass
    
    outPath = resultRootDir+'results'+'/'+'datasets'+str(highDim)+str(lowDim)+'BAR'+'.png'
    
    ind = np.arange(nDataset)  # the x locations for the groups
    width = 0.35       # the width of the bars
    maxf1 = np.max(f1Avgscoretable)+0.05
    minf1 = np.min(f1Avgscoretable)-0.05
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, f1Avgscoretable[:,0], width, color='y',label='SPCA')
    rects2 = ax.bar(ind+width, f1Avgscoretable[:,1], width, color='k',label='SSPCA')
    #rects3 = ax.bar(ind+width+width, accResult[1,:], width, color='b',label='FCM')
    ax.legend( (rects1[0], rects2[0]), ('SPCA', 'SSPCA') )
       
    ax.set_xticks(ind+width)
        
    plt.xlabel('Data sets',size='large')
    plt.ylabel('F1_score',size='large')
#    plt.title('%s Performance: %s ' % (title,dataset))
    plt.title('%s->%s ' %(str(highDim),str(lowDim)) ,size='large')
    plt.legend(loc="upper right")
    plt.ylim([minf1,maxf1])
    #ax.set_xticks(np.arange(1,(nXTicks+2)))
    ax.set_xticklabels([str(i) for i in datasets],rotation=0,size='medium',ha='center')
    plt.savefig(outPath,format='png')
    plt.show()
    
    pass
if __name__=='__main__':
#    plotsspcaresult()
    plotsspcaDatasetBar()