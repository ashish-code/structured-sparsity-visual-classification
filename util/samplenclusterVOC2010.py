#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       samplenclusterVOC2010.py
#       

import os
import numpy as np
from scipy.cluster.vq import kmeans2,vq

#dataSets = ['Caltech101','Caltech256','Scene15','VOC2006','VOC2007','VOC2010']
dataSets=['VOC2010']
rootPath = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureSubspace/'
cbDir = '/'
bofDir = '/BOF/'
nSamples = 500000 # approximate number of samples from dataset
nCodewords = 1000   # number of codebooks
nIterKmeans = 20   # number of iterations of kmeans2
mInit = 'random'    # method of initialization of kmeans2
codebookext = '.cb'
bofext = '.bof'

def main():
	for dataset in dataSets:
		dataPath = rootPath+dataset+dataDir
		catlist = os.listdir(dataPath)
		nCategories = len(catlist)
		nSamplesPerCat = int(np.round(nSamples/nCategories))
		count=0
		for cat in catlist:
			catfilePath = dataPath+cat
			catname = cat.split('.')[0]
			catData = np.genfromtxt(catfilePath,dtype='float',usecols=np.arange(2,15))
			if(catData.shape[0] <= nSamplesPerCat):
				catSample = catData
			else:
				rndsample = np.random.randint(0,catData.shape[0],nSamplesPerCat)
				catSample = catData[rndsample,:]
			if(count==0):
				cumData = catSample
			else:
				cumData = np.concatenate((cumData,catSample),axis=0)
			count+=1
		# compute the codebook for the dataset
		[CodeBook,label] = kmeans2(cumData,nCodewords,iter=nIterKmeans,minit='points',missing='warn')
		# write codebook to file
		cbfilepath = rootPath+dataset+cbDir+dataset+codebookext
		cbfile = open(cbfilepath,'w')
		np.savetxt(cbfile,CodeBook,fmt='%f', delimiter=' ',)
		cbfile.close()
		# compute the bag-of-features histogram for each image
		for cat in catlist:
			catfilePath = dataPath+cat
			catname = cat.split('.')[0]
			catData = np.genfromtxt(catfilePath,dtype='float',usecols=np.arange(2,15))
			[catLabel,catDist] = vq(catData,CodeBook)
			catImgId = np.genfromtxt(catfilePath,dtype=np.int,usecols=np.arange(15,16))
			catId = np.genfromtxt(catfilePath,dtype=np.int,usecols=np.arange(16,17))[0]
			ImgId = np.unique(catImgId)
			catboffilepath = rootPath+dataset+bofDir+catname+bofext
			catboffile = open(catboffilepath,'w')
			imgcount=0
			for imgid in ImgId:
				imgLabel = catLabel[catImgId==imgid]
				[hist,edges] = np.histogram(imgLabel,nCodewords)
				if imgcount==0:
					dataout = np.hstack((hist.T,imgid,catId))
				else:
					dataout = np.vstack((dataout,np.hstack((hist.T,imgid,catId))))
				imgcount+=1
				print('%s : %s' % (catname,imgid))
			np.savetxt(catboffile, dataout, fmt='%d', delimiter=' ', )
			catboffile.close()	
	return 0

if __name__ == '__main__':
	main()

