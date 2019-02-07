#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       samplencluster.py
#       

import os
import numpy as np
from scipy.cluster.vq import kmeans2

dataSets = ['Caltech101','Caltech256','Scene15','VOC2006','VOC2007','VOC2010']

rootPath = '/vol/vssp/diplecs/ash/Data/'
dataDir = '/FeatureSubspace/'
cbDir = '/Codebook/'
bofDir = '/BOF/'
nCodewords = 1000   # number of codebooks
nIterKmeans = 20   # number of iterations of kmeans2
mInit = 'random'    # method of initialization of kmeans2
codebookext = '.cb'
bofext = '.bof'



def samplencluster():
	
	pass

if __name__ == '__main__':
	samplencluster()

