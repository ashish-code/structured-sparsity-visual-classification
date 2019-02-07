#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 Ashish Gupta <ag00087@cvplws32>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



import os
import string
import csv
import numpy as np

def main():
	rootDir = '/vol/vssp/diplecs/ash/Data/'
	dataset = 'Caltech256'
	dataDir = rootDir+dataset+'/'+'Feature'+'/'
	outDir = rootDir+dataset+'/'+'FeatureMatrix'+'/'
	catlist = os.listdir(dataDir)
	# acquire category id number
	catidlist = rootDir+dataset+'/'+dataset+'.txt'
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
	return 0

if __name__ == '__main__':
	main()

