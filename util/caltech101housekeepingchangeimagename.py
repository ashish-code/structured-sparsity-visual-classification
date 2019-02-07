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
def main():
	dataDir = '/vol/vssp/diplecs/ash/Data/Caltech101/ImagesJPG/'
	listcat = os.listdir(dataDir)
	for catname in listcat:
		catDir = dataDir+catname
		os.chdir(catDir)
		listimgs = os.listdir(catDir)
		print catname
		for imgnameold in listimgs:
			if string.count(imgnameold,'_')==1:
				imgnamenew = imgnameold.split('_')[1]
				os.rename(imgnameold,imgnamenew)
	return 0

if __name__ == '__main__':
	main()

