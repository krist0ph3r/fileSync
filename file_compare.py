#!/usr/bin/python
import sys
import os

def addfile(file):
    if file[1] in allfiles:
        allfiles[file[1]].append(file[0])
    else:
        allfiles[file[1]] = [file[0]]

def scanfiles(dir):
    for dirName, subdirList, fileList in os.walk(dir):
        for fname in fileList:
            fullpath = '%s/%s' % (dirName , fname)
            size = os.path.getsize(fullpath)
            addfile((fullpath,size))
        #if len(subdirList) > 0:
            #del subdirList[0]
            #for subdir in subdirList:
            #    print('%s/%s' % (dirName , subdir))

rootDir = sys.argv[1]
allfiles = {}
scanfiles(rootDir)

for file in allfiles:
    print(file,allfiles[file])

