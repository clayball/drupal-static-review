#!/usr/bin/env python


import sys
import os
import mmap
from os import listdir
from os.path import isfile, join, isdir

def getAllFilesRecursive(root):
    files = [ join(root,f) for f in listdir(root) if isfile(join(root,f))]
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                files.append(join(root,f))
    return files

def mainf(root):
    arrayList = getAllFilesRecursive(root)
    for items in arrayList:
        f = open(items)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find("$form_state['values']") != -1:
            print '\nFound on this file ******'
            print items
        else:
            print '\nNot found on file '
            print items


if __name__ == "__main__":
    try:
        module_path = sys.argv[1]
        mainf(module_path)
    except IndexError:
        print("Usage: CodeAssist.py <path to module folder>")
        print("Ie: /root/Desktop/Security_Review/metatag")
    exit(0)
