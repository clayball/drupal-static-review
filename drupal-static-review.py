#!/usr/bin/env python

# - Open file and search for string.. display each line number the string is
# found on.
# - Use a searchString list instead of a single string
# - Search multiple files
# - Add count of each string found (summary details)

import sys
import os
import yaml

# Local file variables (global)
infiles = []


# Local functions

# Static report
def find_search_strings():
    print '[+] searching for search string strings..'
    report = ''
    for infile in infiles:
        # print '[debug] infile: ', infile
        with open(infile) as reviewFile:
            # print '[debug] reviewFile ', reviewFile
            for num, line in enumerate(reviewFile, 1):
                for s in searchStrings:
                    if s in line:
                        print '[+]', s, 'at line:', num, '\t', line.lstrip()
                        report += infile + ' ' + s + ' at line: ' + str(num) + '\n' + line.lstrip() + '\n\n'
            report += '[*] End report for ' + infile + '\n'
            report += '=== \n\n'
    return report


# Menu report
def find_menu_paths():
    print '[+] finding menu paths..'


def find_all_files():
    print '[+] finding all files..'
    for root, dirs, files in os.walk(fullPath):
        for file in files:
            if file.endswith(".module") or file.endswith(".inc") or file.endswith(".install") or file.endswith(".php"):
                print(os.path.join(root, file))
                infiles.append(os.path.join(root, file))


def create_staticreport_header():
    report_header = ''
    report_header = 'Static Report for ' + moduleName + '\n'
    report_header += 'Search type: ' + searchType + '\n'
    report_header += '==================================================\n\n'
    if debugMessages == True:
        print '\n\n' + report_header
    return report_header


def create_menureport_header():
    report_header = None
    report_header = 'Menu Report for ' + moduleName + '\n'
    report_header += '==================================================\n\n'
    if debugMessages == True:
        print '\n\n' + report_header
    return report_header


sqlSearch = ["mysql", "query"]
inputSearch = ["$form_state", "_GET", "_POST", "_REQUEST"]
# not including t(), st()
sanitizationSearch = ["check_markup", "check_plain", "check_url", "drupal_attributes",
                      "drupal_strip_dangerous_protocols", "filter_xss", "format_string", "get_t"]

# Main section

# get arguments
moduleName = sys.argv[1]

# Allow search for specific types of strings, e.g. sql, or all if len(sys.argv[2]):
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

##############################################################################
# Static Report

# Find all the strings we are interested in
stringReport = find_search_strings()

# Create the staticReport header
staticHeader = create_staticreport_header()

# Write the static report data
fs = open('reports/' + moduleName + '-static-' + searchType + '.txt', 'w')
fs.write(staticHeader)
fs.write(stringReport)
fs.close()

##############################################################################
# Menu Report
#
# Find all of the menu paths and flag those that are admin
menuReport = find_menu_paths()


##############################################################################
# Input Report
#
# TODO: still deciding on whether we should break this out or not.
