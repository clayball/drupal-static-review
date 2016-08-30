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
def search_file(search_strings, s, items, length):
    root_item = items
    root_item = root_item.split('/', -1)[-1]
    report_content = '===============================================================================\n'
    report_content += '=\n'
    report_content += '=    Report for ' + root_item + '\n'
    report_content += '=\n'
    report_content += '===============================================================================\n\n'
    for queries in search_strings:
        is_bad = 0
        if debug_messages == True:
            print '[+] queries: %s' % queries
        if s.find(queries) != -1:
            if debug_messages == True:
                print '[+] queries != -1: %s' % queries
            # check if the found string is a good, bad, or sqli string
            # is_bad = check_is_bad(queries, s)
            # if is_bad == 1:
            #     module_status = '****** Found: BAD STRING ****** ' + queries
            # else:
            #     is_sqli = check_is_sqli(queries, s)
            #     if is_sqli == 1:
            #         module_status = '****** Found: SQLI STRING ****** ' + queries
            #     else:
            module_status = '*** Found: STRING *** ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            report_content += module_status + module_path
        else:
            module_status = 'Did not find ' + queries
            module_path = ' in ' + cutit(items, length) + '\n\n'
            report_content += module_status + module_path
    return report_content


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


# check if the found string is in bad_strings
def check_is_bad(queries, s):
    found = 0
    bad_strings = content_yaml['bad_strings']
    #if debug_messages == True:
        #print '[+] Debug: bad_strings %s' % bad_strings
    for query in queries:
        if s.find(query) != -1:
            if debug_messages == True:
                print '[+] Debug: found bad string'
                found = 1
    return found


# check if the found string is in bad_strings
def check_is_sqli(queries, s):
    found = 0
    sqli_strings = content_yaml['sqli_strings']
    if debug_messages == True:
        print '[+] Debug: sqli_strings %s' % sqli_strings
    for q in queries:
        if s.find(q) != -1:
            if debug_messages == True:
                print '[+] Debug: found sqli string'
                found = 1
    return found


# TODO: add description
#       add check if the identified string is a good thing or a bad thing, e.g., eval() is BAD
def mainf(module_name):
    #with open('./config/config.yaml', 'r') as z:
    #    content_yaml = yaml.load(z)
    #root = content_yaml['review_dir']
    filetypes = content_yaml['review_filetype']

    #debug_messages = content_yaml['debug_messages']
    if debug_messages == True:
        print "[+] search_strings %s\n" % search_strings
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
        content += search_file(search_strings, s, items, length)
    fs = open('reports/' + module_name + '.txt', 'w' )
    fs.write(content)
    fs.close()
    print content


# Clean user input
# Python should have a module/library that does this.
# TODO: add sanitization and validation code
def clean_user_args():
    if debug_messages == True:
        print '[+] Debug: begin clean_user_args\t \t \t \t[OK]'
    return 1


# This is our main module. Execution starts here.
if __name__ == "__main__":
    try:
        module_name = sys.argv[1]
        # sanitize and validate user input TODO
        # remove print lines after testing.
        with open('./config/config.yaml', 'r') as z:
            content_yaml = yaml.load(z)
        root = content_yaml['review_dir']
        debug_messages = content_yaml['debug_messages']
        if (clean_user_args() == 1):
            if debug_messages == True:
                print '[+] Debug: good input.\t \t \t \t \t \t[OK]'
            mainf(module_name)
        else:
            print '[!] Warning: something went wrong with cleaning user args.'
            exit(0)
        # allow search for specific types of strings, e.g. sqli_strings, or all
        if sys.argv[2]:
            print("[+] search string: %s") % sys.argv[2]
            searchStrings = sys.argv[2]  # TODO: validate this input
        else:
            searchStrings = "strings"

        search_strings = content_yaml[searchStrings]

    except:
        print("[-] Error: an unknown has occurred.")

    exit(0)

