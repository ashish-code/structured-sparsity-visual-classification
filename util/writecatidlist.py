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

# assign a visual category id number to each category in the dataset

import os
import string

def main():
	rootDir = '/vol/vssp/diplecs/ash/Data/'
	dataset = 'Caltech101'
	dataDir = rootDir+dataset+'/'+'Feature'+'/'
	outDir = rootDir+dataset+'/'
	catlist = os.listdir(dataDir)
	outfile = open(outDir+dataset+'.txt','w')
	catlist.sort(key=string.lower)
	id = 1
	for cat in catlist:
		print cat
		if cat!='BACKGROUND_Google':
			outfile.write(cat+','+str(id)+'\n')
			id += 1
		else:
			outfile.write(cat+','+str(0)+'\n')
	outfile.close()
	return 0

if __name__ == '__main__':
	main()

