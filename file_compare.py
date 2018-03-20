#!/usr/bin/python
import sys
import os
import hashlib
import argparse
from pathlib import Path

scancount = 0
hashcount = 0

def counts(sc=False,hc=False,forceprint=False):
    if sc:
        if forceprint or sc % 117 == 0: sys.stderr.write('%d files scanned\n' % sc)
    if hc:
        hashcount = hc
        if forceprint or hc % 47 == 0: sys.stderr.write('%d files hashed\n' % hc)

def addhashcode(size):
    hashcount = hashcount + 1
    print(scancount,hashcount)
    if unique in allfiles[size]:
        filename = allfiles[size][unique]
        content = Path(filename[0]).read_bytes()
        md5 = hashlib.md5()
        sha = hashlib.sha224()
        md5.update(content)
        sha.update(content)
        allfiles[size].pop(unique)
        hash = md5.hexdigest() + "_" + sha.hexdigest()
        if hash in allfiles[size]:
            allfiles[size][hash].append(filename[0])
        else:
            allfiles[size][hash] = filename
        counts(hc=hashcount)

def addfile(filename, size):
    scancount = scancount + 1
    if size in allfiles:
        addhashcode(size)
        allfiles[size][unique] = [filename]
        addhashcode(size)
    else:
        allfiles[size] = {}
        allfiles[size][unique]=[filename]
    counts(sc=scancount)

def scanfiles(dir):
    for dirName, subdirList, fileList in os.walk(dir):
        for fname in fileList:
            fullpath = '%s/%s' % (dirName , fname)
            size = os.path.getsize(fullpath)
            addfile(fullpath,size)

def presentresults(args):
    print(scancount,hashcount)
    counts(scancount,hashcount,True)
    for size in allfiles:
        for hash in allfiles[size]:
            if len(allfiles[size][hash]) > 1:
                if args.duplicate: print('%s: %s' % (duplicate, ','.join(allfiles[size][hash])))
            else:
                if args.unique: print('%s: %s' % (unique, ','.join(allfiles[size][hash])))
    if args.map:
        for file in allfiles:
            print(file,allfiles[file])


parser = argparse.ArgumentParser(description='Scan directories for duplicates and unique files', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-m', '--map', dest='map', default=False, action='store_true', help='print the raw map')
parser.add_argument('-u', '--unique', dest='unique', default=False, action='store_true', help='print unique files')
parser.add_argument('-d', '--duplicate', dest='duplicate', default=False, action='store_true', help='print duplicate files')
parser.add_argument('path', nargs='+', help='Paths of directories to scan')
args = parser.parse_args()

allfiles = {}
unique = 'unique'
duplicate = 'duplicate'

for rootDir in args.path:
    scanfiles(rootDir)
presentresults(args)

