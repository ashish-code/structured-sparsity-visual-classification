#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       writefeaturevectorVOC2010.py
#       

import os
import string
import numpy as np
import csv

def main():
	rootDir = '/vol/vssp/diplecs/ash/Data/'
	dataSets = ['VOC2010']
	imageSets = '/ImageSets/Main/'
	outDir = '/FeatureMatrix/'
	inDir = '/Feature/'
	ftype = '.sift'
	#loop through each dataset
	for dataset in dataSets:
		fcatid=rootDir+dataset+'/'+'catidlist.txt'
		catnames=np.genfromtxt(fcatid,usecols=[0],dtype='string',delimiter=',')
		catids=np.genfromtxt(fcatid,usecols=[1],dtype='int',delimiter=',')
		cats = dict(zip(catnames,catids))
		for catname in cats.keys():
			outfilename = rootDir+dataset+outDir+catname+ftype
			outfile = open(outfilename,'w')
			catimgsetfilename = rootDir+dataset+imageSets+catname+'_trainval.txt'
			imgnames=np.genfromtxt(catimgsetfilename,usecols=[0],dtype='string')
			imgids=np.genfromtxt(catimgsetfilename,usecols=[1],dtype='int')
			images=dict(zip(imgnames,imgids))
			for imgname in images:
				if(images.get(imgname)==1):
					#open the imgname file and write to the outfile
					featfilename=rootDir+dataset+inDir+imgname+ftype
					featdata=np.loadtxt(featfilename,delimiter=' ',skiprows=2,\
					dtype=np.int,usecols=np.concatenate((np.arange(0,2),np.arange(5,133))))
					imgnameX = str(imgname.split('_')[0])[2:4]
					imgnameY = str(imgname.split('_')[1])[2:6]
					imgnameID = imgnameX+imgnameY
					for vector in featdata:
						for elem in vector:
							outfile.write('%d ' % elem)		
						outfile.write('%s %d\n' % (imgnameID,cats.get(catname)))
					print(dataset + ' : ' + catname + ' : ' + imgnameID)
			outfile.close()
	return 0

if __name__ == '__main__':
	main()

