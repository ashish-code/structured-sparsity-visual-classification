#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       writecatidlistScene15.py
#       

import os
import string

def main():
	rootDir = '/vol/vssp/diplecs/ash/Data/'
	dataset = 'Scene15'
	dataDir = rootDir+dataset+'/Feature/'
	outDir = rootDir+dataset+'/'
	catlist = os.listdir(dataDir)
	outfile = open(outDir+'catidlist.txt','w')
	catlist.sort(key=string.lower)
	id=0
	for cat in catlist:
		id+=1
		outfile.write('%s,%d\n' % (cat,id))
		print(cat + ' : ' + str(id))
	outfile.close()
	return 0

if __name__ == '__main__':
	main()

