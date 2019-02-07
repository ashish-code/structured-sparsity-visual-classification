'''
Created on 24 Nov 2011

@author: ag00087
'''

import os
dataSets = ['Birds','Butterflies','Flowers17','Flowers102','UIUC']
dataDir = '/ImagesPNG/'
rootDir = '/vol/vssp/diplecs/ash/Data/'

def writeCategoryList(dataSet):
    dataPath = rootDir+dataSet+dataDir
    categoryListFileName = rootDir+dataSet+'/categoryList.txt'
    catidListFileName = rootDir+dataSet+'/catidlist.txt'
    categoryListFile = open(categoryListFileName,'w')
    catidListFile = open(catidListFileName,'w')
    if(dataSet == 'Flowers17'):
        for i in xrange(17):
            categoryName = str(i+1)
            iCategory = i
            print categoryName
            categoryListFile.write(categoryName+'\n')
            catidListFile.write(categoryName+','+str(iCategory+1)+'\n')
        pass
    elif(dataSet == 'Flowers102'):
        for i in xrange(102):
            categoryName = str(i+1)
            iCategory = i
            print categoryName
            categoryListFile.write(categoryName+'\n')
            catidListFile.write(categoryName+','+str(iCategory+1)+'\n')
        pass
    elif(dataSet == 'UIUC'):
        categoryName = 'car'
        iCategory = 0
        print categoryName
        categoryListFile.write(categoryName+'\n')
        catidListFile.write(categoryName+','+str(iCategory+1)+'\n')
        pass
    else:
        for dirname,dirnames,filenames in os.walk(dataPath):
            for iCategory,categoryName in enumerate(dirnames):
                print categoryName
                categoryListFile.write(categoryName+'\n')
                catidListFile.write(categoryName+','+str(iCategory+1)+'\n')
        pass
    categoryListFile.close()
    catidListFile.close()
    pass
if __name__ == '__main__':
    for dataSet in dataSets:
        print dataSet
        writeCategoryList(dataSet)