#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cbnbofCaltech101.py
#       

import os
import numpy as np
from scipy.cluster.vq import kmeans2

#dataSets = ['Caltech101','Caltech256','Scene15','VOC2006','VOC2007','VOC2010']
dataSets=['VOC2006']
rootPath = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureSubspace/'
cbDir = '/Codebook/'
bofDir = '/BOF/'
nCodewords = 1000   # number of codebooks
nIterKmeans = 100   # number of iterations of kmeans2
mInit = 'random'    # method of initialization of kmeans2
codebookext = '.cb'
bofext = '.bof'


def main():
	for dataset in dataSets:
		dataPath = rootPath+dataset+dataDir
		catlist = os.listdir(dataPath)
		for cat in catlist:
			catfilePath = dataPath+cat
			catname = cat.split('.')[0]
			catData = np.genfromtxt(catfilePath,dtype='float',usecols=np.arange(2,15))
			[catCodebook,catLabel] = kmeans2(catData,nCodewords,iter=nIterKmeans,minit='points',missing='warn')
			catImgId = np.genfromtxt(catfilePath,dtype=np.int,usecols=np.arange(15,16))
			catId = np.genfromtxt(catfilePath,dtype=np.int,usecols=np.arange(16,17))[0]
			ImgId = np.unique(catImgId)
			catcbfilepath = rootPath+dataset+cbDir+catname+codebookext
			catboffilepath = rootPath+dataset+bofDir+catname+bofext
			catcbfile = open(catcbfilepath,'w')
			catboffile = open(catboffilepath,'w')
			imgcount=0
			for imgid in ImgId:
				imgLabel = catLabel[catImgId==imgid]
				[hist,_] = np.histogram(imgLabel,nCodewords)
				if imgcount==0:
					dataout = np.hstack((hist.T,imgid,catId))
				else:
					dataout = np.vstack((dataout,np.hstack((hist.T,imgid,catId))))
				imgcount+=1
				print('%s : %s' % (catname,imgid))
			np.savetxt(catboffile, dataout, fmt='%d', delimiter=' ', )
			np.savetxt(catcbfile,catCodebook,fmt='%f', delimiter=' ',)
			catcbfile.close()
			catboffile.close()	
					
	return 0

if __name__ == '__main__':
	main()

