#!/usr/bin/env python

# - Open file and search for string.. display each line number the string is
# found on.
# - Use a searchString list instead of a single string
# - Search multiple files
# - Add count of each string found (summary details)

import sys
import os
import yaml

# ######### LOCAL VARIABLES #########
infiles = []


# ######### LOCAL FUNCTIONS #########

# Static report
# TODO: work on fine-tuning this over time.
def find_search_strings():
    print '[+] Searching for strings of interest..'
    report = ''
    total_hits = 0
    for infile in infiles:
        hitsinfile = 0
        # print '[debug] infile: ', infile
        with open(infile) as reviewFile:
            # print '[debug] reviewFile ', reviewFile
            for num, line in enumerate(reviewFile, 1):
                for s in searchStrings:
                    if s in line:
                        hitsinfile += 1
                        total_hits += 1
                        print '[+]', s, 'at line:', num, '\t', line.lstrip()
                        report += infile + ' ' + s + ' at line: ' + str(num) + '\n' + line.lstrip() + '\n\n'
            # Only print this for files that contain code of interest.
            if hitsinfile > 0:
                report += '[*] Found ' + str(hitsinfile) + ' hits in ' + infile + '\n'
                report += '=== \n\n'
    report += '========================================'
    report += 'Summary Details\n'
    report += 'Total locations found: ' + str(total_hits) + '\n'
    return report


# Menu report
def find_menu_paths():
    print '[+] finding menu paths..'
    menupaths = ['TODO']
    return menupaths


# Find all files to be searched
def find_all_files():
    print '[+] finding all files..'
    for root, dirs, files in os.walk(fullPath):
        for f in files:
            if f.endswith(".module") or f.endswith(".inc") or \
                    f.endswith(".install") or f.endswith(".php"):
                print(os.path.join(root, f))
                infiles.append(os.path.join(root, f))


# Report header
def create_staticreport_header():
    report_header = ''
    report_header = 'Static Report for ' + moduleName + '\n'
    report_header += 'Search type: ' + searchType + '\n'
    report_header += '==================================================\n\n'
    if debugMessages:
        print '\n\n' + report_header
    return report_header


# Menu report header
def create_menureport_header():
    report_header = None
    report_header = 'Menu Report for ' + moduleName + '\n'
    report_header += '==================================================\n\n'
    if debugMessages:
        print '\n\n' + report_header
    return report_header


# ######### MAIN PROGRAM #########

# get arguments
moduleName = sys.argv[1]

# Allow search for specific types of strings, e.g. sql, or all if
# len(sys.argv[2]):
try:
    searchType = sys.argv[2]
except:
    searchType = "full"

# Read settings from config file
try:
    with open('./config/config.yaml', 'r') as setting:
        contentYaml = yaml.load(setting)
except:
    print "[-] TODO: add error message"
    exit(0)

codeDirectory = contentYaml['review_dir']
searchStrings = contentYaml[searchType]
debugMessages = contentYaml['debug_messages']
fileTypes = contentYaml['review_filetypes']
print "[*] Performing %s search on %s" % (searchType, moduleName)
print "[*]  located in %s" % codeDirectory

fullPath = codeDirectory + '/' + moduleName

# Find all of the files we are interested in searching
find_all_files()

# #############
# Static Report
# #############

# Find all the strings we are interested in
stringReport = find_search_strings()

# Create the staticReport header
staticHeader = create_staticreport_header()

# Write the static report data
fs = open('reports/' + moduleName + '-static-' + searchType + '.txt', 'w')
fs.write(staticHeader)
fs.write(stringReport)
fs.close()

# ###########
# Menu Report
# ###########
# TODO: still deciding on whether we should break this out to another script
#       or not.
# Find all of the menu paths and flag those that are admin
#menuReport = find_menu_paths()


##############
# Input Report
# ############
