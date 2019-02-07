'''
Created on 18 Jan 2012

@author: ag00087
'''

import numpy as np
from sklearn import svm
from sklearn.metrics import roc_curve, auc, f1_score, precision_score, recall_score, precision_recall_curve
from sklearn.cross_validation import StratifiedKFold

rootDir = '/vol/vssp/diplecs/ash/Data/'
iwmDir = '/ImgWrdMat/'
pcaDir = '/PCA/'
resultRootDir = '/vol/vssp/diplecs/ash/Expt/sspca/'

dataset = 'Scene15'
catName = 'store'
highDim = 1024
lowDim = 64
method = 'spca'

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
    probas_ = clsProb.fit(X[train],y[train]).predict_proba(X[test])
    pred = cls.fit(X[train],y[train]).predict(X[test])
    # Compute ROC curve and area the curve
    rocfpr, roctpr, rocthresh = roc_curve(y[test], probas_[:,1])
    roc_aucArr[i] = auc(rocfpr, roctpr)
    pre, rec, prthresh = precision_recall_curve(y[test], probas_[:, 1])
    pr_aucArr[i] = auc(rec, pre)
    f1scoreArr[i] = f1_score(y[test],pred,pos_label=1)
    precisionArr[i] = precision_score(y[test],pred,pos_label=1)
    recallArr[i] = recall_score(y[test],pred,pos_label=1)
    pass

print np.mean(roc_aucArr)
print np.std(roc_aucArr)
print np.mean(pr_aucArr)
print np.std(pr_aucArr)
print np.mean(f1scoreArr)