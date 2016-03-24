#!/usr/bin/env python


import sys
import os
import yaml
import mmap
from os import listdir
from os.path import isfile, join, isdir



def searchMe(searchString, s, items, length):
    root_item = items
    root_item = root_item.split('/', -1)[-1]
    reportContent = 'This is the report of the file ' + root_item + '\n'
    reportContent += '====================================\n'
    for queries in searchString:
        if s.find(queries) != -1:
            module_status = '******************* Found ******************* ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            reportContent += module_status + module_path
        else:
            module_status = 'Did not find ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            reportContent += module_status + module_path
    return reportContent


def cutit(s,n):    
   return s[n:]

def getAllFilesRecursive(root):
    files = [ join(root,f) for f in listdir(root) if isfile(join(root,f))]
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                files.append(join(root,f))
    return files

def mainf(module_name):
    with open('./config/config.yaml', 'r') as z:
        content_yaml = yaml.load(z)
    root = content_yaml['review_dir']
    filetypes = content_yaml['review_filetype']
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
        searchString = ["$form_state['values']", "$form_state['input']", "eval", "mysql", "query", "$_GET", "$_POST", "$_REQUEST", "check_plain", "xss", "check_markup"]
        content += searchMe(searchString, s, items, length)
    fs = open( module_name + '.txt', 'w' )
    fs.write(content)
    fs.close()
    print content


if __name__ == "__main__":
    try:
        module_name = sys.argv[1]
        mainf(module_name)
    except IndexError:
        print("Usage: CodeAssist.py <name of module>")
        print("Ie: metatag")
    exit(0)

