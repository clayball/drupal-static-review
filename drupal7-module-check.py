#!/usr/bin/env python

# Clay Wells
# Hoang Bui

# Purpose:
# 
# Identify code fragments that we deem both dangerous and helpful. 
# This is the first step when doing a code review of a Drupal7 contrib module.
# 
# Output:
#
# Text file reporting all identified code fragments.


import sys
import os
import yaml
import mmap
from os import listdir
from os.path import isfile, join, isdir


# Define our modules here
def searchMe(searchString, s, items, length):
    root_item = items
    root_item = root_item.split('/', -1)[-1]
    reportContent = 'This is the report of the file ' + root_item + '\n'
    reportContent += '=========================================================================================\n'
    for queries in searchString:
        if s.find(queries) != -1:
            module_status = '********** FOUND ********** ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            reportContent += module_status + module_path
        else:
            module_status = 'Did not find ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            reportContent += module_status + module_path
    return reportContent


# TODO: add description
def cutit(s,n):    
   return s[n:]


# TODO: add description
def getAllFilesRecursive(root):
    files = [ join(root,f) for f in listdir(root) if isfile(join(root,f))]
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                files.append(join(root,f))
    return files


# TODO: add description
def mainf(module_name):
    with open('./config/config.yaml', 'r') as z:
        content_yaml = yaml.load(z)
    root = content_yaml['review_dir']
    filetypes = content_yaml['review_filetype']
    search_strings = content_yaml['search_strings']
    full_path = root + '/' + module_name
    length = len(full_path)
    arrayList = getAllFilesRecursive(full_path)
    new_arrayList = []
    for file in arrayList:
        tempFile = file
        for filetype in filetypes:
            if file.split('.', -1)[-1] == filetype:
                new_arrayList += [file]
    content = ''
    for items in new_arrayList:
        f = open(items)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        content += searchMe(search_strings, s, items, length)
    fs = open( module_name + '.txt', 'w' )
    fs.write(content)
    fs.close()
    print content


# Clean user input
# Python should have a module/library that does this.
# TODO: add sanitization and validation code
def clean_user_args():
    print '[+] in clean_user_args'
    return 1


# This is our main module. Execution starts here.
if __name__ == "__main__":
    try:
        module_name = sys.argv[1]
        # sanitize and validate user input TODO
        # remove print lines after testing.
        if (clean_user_args() == 1):
            print '[+] Check: clean input, continue. %t %t %t [OK]'
        else:
            print '[!] Warning: something went wrong with cleaning user args.'
            exit(0)
        
        mainf(module_name)
    except IndexError:
        print("Usage: CodeAssist.py <name of module>")
        print("Ie: metatag")
    exit(0)

