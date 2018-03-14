#!/usr/bin/python
import sys
import os
import hashlib
from pathlib import Path


def addhashcode(size):
    if unique in allfiles[size]:
        filename = allfiles[size][unique]
        m = hashlib.md5()
        m.update(Path(filename[0]).read_bytes())
        allfiles[size].pop(unique)
        hash = m.hexdigest()
        if hash in allfiles[size]:
            allfiles[size][hash].append(filename[0])
        else:
            allfiles[size][hash] = filename

def addfile(filename, size):
    if size in allfiles:
        addhashcode(size)
        allfiles[size][unique] = [filename]
        addhashcode(size)
    else:
        allfiles[size] = {}
        allfiles[size][unique]=[filename]

def scanfiles(dir):
    for dirName, subdirList, fileList in os.walk(dir):
        for fname in fileList:
            fullpath = '%s/%s' % (dirName , fname)
            size = os.path.getsize(fullpath)
            addfile(fullpath,size)

rootDir = sys.argv[1]
allfiles = {}
unique = 'unique'
scanfiles(rootDir)

for file in allfiles:
    print(file,allfiles[file])

