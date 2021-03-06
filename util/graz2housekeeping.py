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
import shutil
def main():
	dataDir = '/vol/vssp/diplecs/ash/Data/Graz2/'
	outDir = '/vol/vssp/diplecs/ash/Data/Graz2/ImagesJPG/'
	catnames = os.listdir(dataDir)
	for catname in catnames:
		if catname!='ImagesJPG':
			catDir = dataDir+catname+'/'+catname+'/'
			os.chdir(catDir)
			flist = os.listdir(catDir)
			print catname
			for fname in flist:
				if string.count(fname,'image')==1:
					shutil.copy(catDir+fname,outDir+catname)
					print fname
	return 0

if __name__ == '__main__':
	main()

