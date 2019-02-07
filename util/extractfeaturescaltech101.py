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


import os.path


def main():
	dataDir = '/vol/vssp/diplecs/ash/Data/Caltech101/ImagesPNG/'
	catlist = os.listdir(dataDir)
	progDir = '/vol/vssp/diplecs/ash/code/descriptorvgg/'
	prog = 'extract_features.ln'
	featureDir = '/vol/vssp/diplecs/ash/Data/Caltech101/Feature/'
	#paramDir = '/vol/vssp/diplecs/ash/Data/Caltech101/Params/'
	for catname in catlist:
		catDir = dataDir+catname
		os.chdir(catDir)
		imglist = os.listdir(catDir)
		featureCatDir = featureDir+catname+'/'

		if not os.path.isdir(featureCatDir):
			os.mkdir(featureCatDir)
		
		for img in imglist:
			if(img.split('.')[1]=='png'):
				featureName = img.split('.')[0]+'.sift'
				featureFile = featureCatDir+featureName
				com = progDir+prog+' -harlap -sift'+' -i '+img+' -o1 '+featureFile
				os.system(com)
				print(catname + ' : '+featureName)
				paramfilename = featureCatDir+img+'.params'
				commanddel = 'rm '+ paramfilename
				if os.path.exists(paramfilename):
					os.system(commanddel)
			elif(img.split('.')[1]=='jpg'):
				commanddel = 'rm '+img
				os.system(commanddel)	
	return 0

if __name__ == '__main__':
	main()

