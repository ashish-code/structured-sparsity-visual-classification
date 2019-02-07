'''
Created on 18 Jan 2012

@author: ag00087
'''

import numpy as np
from optparse import OptionParser
import sys
from sklearn import svm
from sklearn.metrics import roc_curve, auc, f1_score, precision_score, recall_score, precision_recall_curve
from sklearn.cross_validation import StratifiedKFold

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

#global paths
rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'

#global variables
catidfname = 'catidlist.txt' # list of categories in the dataset

def getCatMap(dataset):
    catidfpath = rootDir+dataset+'/'+catidfname
    catnames = np.genfromtxt(catidfpath,delimiter=',',dtype='|S32',usecols=[0])
    catnum = np.genfromtxt(catidfpath,delimiter=',',dtype=np.int,usecols=[1])
    catmap = dict(zip(catnames,catnum))
    return catmap

def computeSVMscore(highDim,lowDim):
    (options, args) = parser.parse_args(sys.argv[1:]) #@UnusedVariable
    dataset = options.dataset
    method = options.method
    #acquire the category list    
    computePerformanceMetrics(dataset,method,highDim,lowDim)
    '''pca'''
    '''
    try:
        print 'pca'
        computePerformanceMetrics(dataset,'pca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'pca',highDim,lowDim)
    
    try:
        print 'ppca'
        computePerformanceMetrics(dataset,'ppca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'ppca',highDim,lowDim)
    
    try:
        print 'rpca'
        computePerformanceMetrics(dataset,'rpca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'rpca',highDim,lowDim)
    
    try:
        print 'kpca'
        computePerformanceMetrics(dataset,'kpca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'kpca',highDim,lowDim)
    
    try:
        print 'spca'
        computePerformanceMetrics(dataset,'spca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'spca',highDim,lowDim)
    
    try:
        print 'sspca'
        computePerformanceMetrics(dataset,'sspca',highDim,lowDim)
    except:
        print 'error:%s:%s:%d:%d'%(dataset,'sspca',highDim,lowDim)
    '''        
    pass
    
def computePerformanceMetrics(dataset,method,highDim,lowDim):
    catmap = getCatMap(dataset)
    catList = catmap.keys()
    nCategory = len(catList)
    #roc_aucAvg = np.zeros((nCategory,1),np.float)
    #roc_aucStd = np.zeros((nCategory,1),np.float)
    #pr_aucAvg = np.zeros((nCategory,1),np.float)
    #pr_aucStd = np.zeros((nCategory,1),np.float)
    f1scoreAvg = np.zeros((nCategory,1),np.float)
    f1scoreStd = np.zeros((nCategory,1),np.float)
    precision = np.zeros((nCategory,1),np.float)
    recall = np.zeros((nCategory,1),np.float)
    for iCat,catName in enumerate(catList):
        pcaDataFileName = rootDir+dataset+pcaDir+catName+str(highDim)+str(lowDim)+'.'+method
        pcaData = np.loadtxt(pcaDataFileName, dtype=np.float,delimiter=' ')
        X = pcaData[:,:-1]
        y = pcaData[:,-1]
        cv = StratifiedKFold(y,k=10)
        clsProb = svm.SVC(kernel='rbf',probability=True)
        cls = svm.SVC(kernel='rbf',probability=False)
        roc_aucArr = np.zeros((10,1),np.float)
        pr_aucArr = np.zeros((10,1),np.float)
        f1scoreArr = np.zeros((10,1),np.float)
        precisionArr = np.zeros((10,1),np.float)
        recallArr = np.zeros((10,1),np.float)
        for i,(train,test) in enumerate(cv):
            #probas_ = clsProb.fit(X[train],y[train]).predict_proba(X[test])
            pred = cls.fit(X[train],y[train]).predict(X[test])
            # Compute ROC curve and area the curve
            #rocfpr, roctpr, rocthresh = roc_curve(y[test], probas_[:,1])
            #roc_aucArr[i] = auc(rocfpr, roctpr)
            #pre, rec, prthresh = precision_recall_curve(y[test], probas_[:, 1])
            #pr_aucArr[i] = auc(rec, pre)
            f1scoreArr[i] = f1_score(y[test],pred,pos_label=1)
            precisionArr[i] = precision_score(y[test],pred,pos_label=1)
            recallArr[i] = recall_score(y[test],pred,pos_label=1)
            pass
        #roc_aucAvg[iCat] = np.mean(roc_aucArr)
        #roc_aucStd[iCat] = np.std(roc_aucArr)
        #pr_aucAvg[iCat] = np.mean(pr_aucArr)
        #pr_aucStd[iCat] = np.mean(pr_aucArr)
        f1scoreAvg[iCat] = np.mean(f1scoreArr)
        f1scoreStd[iCat] = np.std(f1scoreArr)
        precision[iCat] = np.mean(precisionArr)
        recall[iCat] = np.mean(recallArr)
        pass
    #write the results to file
    #roc_aucAvgFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.rocavg'
    #roc_aucStdFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.rocstd'
    #pr_aucAvgFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.pravg'
    #pr_aucStdFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.prstd'
    f1scoreAvgFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.f1avg'
    f1scoreStdFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.f1std'
    precisionFile =resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.pre'
    recallFile = resultRootDir+dataset+'/'+catName+str(highDim)+str(lowDim)+method+'.rec'
    
    #np.savetxt(roc_aucAvgFile, roc_aucAvg, fmt='%f', delimiter=' ')
    #np.savetxt(roc_aucStdFile, roc_aucStd, fmt='%f', delimiter=' ')
    #np.savetxt(pr_aucAvgFile, pr_aucAvg, fmt='%f', delimiter=' ')
    #np.savetxt(pr_aucStdFile, pr_aucStd, fmt='%f', delimiter=' ')
    np.savetxt(f1scoreAvgFile, f1scoreAvg, fmt='%f', delimiter=' ')
    np.savetxt(f1scoreStdFile, f1scoreStd, fmt='%f', delimiter=' ')
    np.savetxt(precisionFile, precision, fmt='%f', delimiter=' ')
    np.savetxt(recallFile, recall, fmt='%f', delimiter=' ')
    pass

if __name__ == '__main__':
    for highDim in higherDims:
        for lowDim in lowerDims:
            if (lowDim <= int(highDim/4)):
                computeSVMscore(highDim,lowDim)
    pass