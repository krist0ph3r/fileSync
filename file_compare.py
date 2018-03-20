#!/usr/bin/python
import sys
import json
import os
import hashlib
import argparse
import socket
from pathlib import Path

def counts(sc=False,hc=False,forceprint=False):
    global scancount
    global hashcount
    if sc:
        scancount = scancount + 1
    if hc:
        hashcount = hashcount + 1
    if forceprint or (args.verbose and sc and scancount % 117 == 0):sys.stderr.write('%d files scanned\n' % scancount)
    if forceprint or (args.verbose and hc and hashcount % 47 == 0):sys.stderr.write('%d files hashed\n' % hashcount)

def addhashcode(size):
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
        counts(hc=True)

def addfile(filename, size):
    if size in allfiles:
        addhashcode(size)
        allfiles[size][unique] = [filename]
        addhashcode(size)
    else:
        allfiles[size] = {}
        allfiles[size][unique]=[filename]
    counts(sc=True)

def scanfiles(dir):
    for dirName, subdirList, fileList in os.walk(dir):
        for fname in fileList:
            fullpath = '%s/%s' % (dirName , fname)
            size = os.path.getsize(fullpath)
            addfile(fullpath,size)

def presentresults(args):
    counts(forceprint=True)
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
parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true', help='verbose mode')
parser.add_argument('-l', '--load', dest='load', action='store', nargs=1, default='', help='preload the map from a file')
parser.add_argument('-s', '--save', dest='save', action='store', nargs=1, default='', help='save the generated map to a file')
parser.add_argument('-p', '--prefix', dest='prefix', action='store', nargs=1, default=socket.gethostname(), help='use prefix to designate current machine (default = hostname)')
parser.add_argument('path', nargs='+', help='Paths of directories to scan')
args = parser.parse_args()

scancount = 0
hashcount = 0
unique = 'unique'
duplicate = 'duplicate'

allfiles = {}
loadflag = args.load != ''
saveflag = args.save != ''
prefix = '%s:' % args.prefix[0] if loadflag or saveflag else ''

if loadflag:
    print('loading from: %s' % args.load[0])
    #with open(args.load) as json_file:
    #    allfiles = json.load(json_file)

print('using prefix: %s' % prefix)

for rootDir in args.path:
    scanfiles(rootDir)

presentresults(args)

if saveflag:
    print('saving to: %s' % args.save[0])
