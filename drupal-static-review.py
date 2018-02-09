#!/usr/bin/env python2

### drupal-static-review.py: Generates a document containing any points of
###                          interest discovered in a module.
###                          Points of interest are defined in the config file.

## Usage ##
#   $ python drupal-static-review.py MODULENAME
# See README for more information.

## General Overview / Notes ##
# 1. Open each file, one at a time, and search for string.
#    Display each line number the string is found on.
# 2. Use a searchString list instead of a single string
# 3. Search multiple files
# 4. Add count of each string found (summary details)


######### IMPORTS #########

import sys
import os
import yaml


######### GLOBAL-SCOPE VARIABLES #########

moduleName = ""
searchType = ""
infiles = []
fullPath = ""
searchStrings = []
debugMessages = False


######### FUNCTIONS #########

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
    report += '========================================\n'
    report += 'Summary Details\n'
    report += 'Total locations found: ' + str(total_hits) + '\n'
    return report


# Menu report
# D8 makes this easy for us.. look inside *.routing.yml file.
def find_menu_paths():
    """
    NOTE: Functionality not currently implemented in Static Review.
    Returns a list of the Menu Paths of the module.
    """
    print '[+] Discovering Menu Paths..'
    menupaths = ['TODO']
    return menupaths


# Find all files to be searched
def find_all_files():
    print '[+] finding all files..'
    for root, dirs, files in os.walk(fullPath):
        for f in files:
            if f.endswith(".module") or f.endswith(".inc") or \
                    f.endswith(".install") or f.endswith(".php") or \
                        f.endswith(".theme") or f.endswith(".twig"):
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


def get_module_arg():
    """Returns arg corresponding to module name.
    If arg doesn't exist, prints error and terminates.
    """
    try:
        return sys.argv[1]
    except:
        print "\n[-] Missing arg! Specify module name.\n"
        exit(1)


def get_type_arg():
    """Returns arg corresponding to search type.
    "Search type" refers to the type of strings (ex sql, xss) 
    to search for. These are defined in the config file.
    If arg doesn't exist, default to a full scan to check for all types.
    """
    try:
        return sys.argv[2]
    except:
        return "full"


def read_config():
    """Returns loaded config yaml file.
    If unable to open config file, prints error and terminates.
    """
    try:
        with open('./config/config.yaml', 'r') as setting:
            return yaml.load(setting)
    except:
        print "\n[-] Unable to open config.yaml!\n"
        exit(2)


######### MAIN PROGRAM #########

def main():
    global moduleName, searchType, fullPath, searchStrings, debugMessages

    # Get arguments.
    moduleName = get_module_arg()
    searchType = get_type_arg()
   
    # Load config file.
    contentYaml = read_config()

    # Read settings from config file
    codeDirectory = contentYaml['review_dir']
    searchStrings = contentYaml[searchType]
    debugMessages = contentYaml['debug_messages']
    fileTypes = contentYaml['review_filetypes']

    print "[*] Performing %s search on %s" % (searchType, moduleName)
    print "[*]  located in %s" % codeDirectory

    fullPath = codeDirectory + '/' + moduleName

    # Find all of the files we are interested in scanning.
    find_all_files()

    ## Static Report ##
    # Find all the strings we are interested in
    stringReport = find_search_strings()
    
    # Create the static report header
    staticHeader = create_staticreport_header()

    # Write the static report data
    fs = open('reports/' + moduleName + '-static-' + searchType + '.txt', 'w')
    fs.write(staticHeader)
    fs.write(stringReport)
    fs.close()


######### PROCESS #########

if __name__ == '__main__':
    main()


# ###########
# Menu Report
# ###########
# TODO: still deciding on whether we should break this out to another script
#       or not.
# Find all of the menu paths and flag those that are admin
#menuReport = find_menu_paths()

