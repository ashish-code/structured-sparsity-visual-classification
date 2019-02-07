#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       writefeaturevectorScene15.py
#       

import os
import csv
import numpy as np

def main():
	rootDir = '/vol/vssp/diplecs/ash/Data/'
	dataset = 'Scene15'
	dataDir = rootDir+dataset+'/'+'Feature'+'/'
	outDir = rootDir+dataset+'/'+'FeatureMatrix'+'/'
	catlist = os.listdir(dataDir)
	# acquire category id number
	catidlist = rootDir+dataset+'/'+'catidlist.txt'
	cr = csv.reader(open(catidlist,'r'),delimiter=',')
	name = []
	catid = []
	for row in cr:
		name.append(row[0])
		catid.append(row[1])
	cats = dict(zip(name,catid))
	
	for cat in catlist:
		catDir = dataDir+cat+'/'
		imglist = os.listdir(catDir)
		outfilename = outDir+cat+'.sift'
		if os.path.exists(outfilename):
			os.remove(outfilename)
		outfile = csv.writer(open(outfilename,'a'),delimiter=' ')
				
		for img in imglist:
			if(img.endswith('sift')):
				imgid = int(img.split('.')[0])
				imgfilename = catDir+img
				imgdata = np.loadtxt(imgfilename,delimiter=' ',dtype=np.int,skiprows=2,usecols=np.concatenate((np.arange(0,2),np.arange(5,133))))
				nvectors = imgdata.shape[0]
				catidarr = int(cats.get(cat))*np.ones(nvectors,dtype=np.int)
				imgidarr = imgid*np.ones(nvectors,dtype=np.int)
				outdata = np.vstack((imgdata.T,imgidarr,catidarr)).T
				outfile.writerows(outdata)
				print(cat + ' : ' + img)
			elif(img.endswith('params')):
				os.remove(catDir+img)
	return 0

if __name__ == '__main__':
	main()

