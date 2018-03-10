#!/usr/bin/python
import sys
import os

rootDir = sys.argv[1]
allfiles = {}

for dirName, subdirList, fileList in os.walk(rootDir):
    #print('Found directory: %s' % dirName)
    for fname in fileList:
        fullpath = '%s/%s' % (dirName , fname)
        size = os.path.getsize(fullpath)
        addfile((fullpath,size))
    # Remove the first entry in the list of sub-directories
    # if there are any sub-directories present
    if len(subdirList) > 0:
        del subdirList[0]

for file in allfiles:
    print(file)

def addfile(file):
    if file[1] in allfiles:
        allfiles[file[1]].append(file[0])
    else:
        allfiles[file[1]] = [file[0]]
