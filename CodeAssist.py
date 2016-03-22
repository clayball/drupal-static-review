#!/usr/bin/env python


import sys
import os
import mmap
def mainf(path):
    listing = os.listdir(path)
    listing_dir = os.listdir(path + '/*')
    fileArray = []
    print "========================================"
    print "These are the files I will run through:"
    print "========================================"
    for infile in listing:
        fileArray += [infile]
        print infile
        fullpath = os.path.join(path, infile)
        f = open(fullpath)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find('blabla') != -1:
            print 'true'

if __name__ == "__main__":
    try:
        module_path = sys.argv[1]
        mainf(module_path)
    except IndexError:
        print("Usage: CodeAssist.py <path to module folder>")
        print("Ie: /root/Desktop/Security_Review/metatag")
    exit(0)
