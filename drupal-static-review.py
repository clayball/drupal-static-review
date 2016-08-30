#!/usr/bin/env python

# - Open file and search for string.. display each line number the string is
# found on.
# - Use a searchString list instead of a single string
# - Search multiple files
# - Add count of each string found (summary details)

import sys
import os
import yaml


def find_all_files():
	print '[+] finding all files.'
	for root, dirs, files in os.walk(fullPath):
		for file in files:
			if file.endswith(".module") or file.endswith(".inc") or file.endswith(".install") or file.endswith(".php") :
				print(os.path.join(root, file))
				infiles.append(os.path.join(root, file))


def create_report_header():
	report_header = 'Static Report for ' + moduleName + '\n'
	report_header += 'Search type: ' + searchType + '\n'
	report_header += '==================================================\n\n'
	if debugMessages == True:
		print '\n\n' + report_header
	return report_header


sqlSearch = ["mysql", "query"]
inputSearch = ["$form_state", "_GET", "_POST", "_REQUEST"]
# not including t(), st()
sanitizationSearch = ["check_markup", "check_plain", "check_url", "drupal_attributes", "drupal_strip_dangerous_protocols", "filter_xss", "format_string", "get_t"]

#infile = 'example.php'
infiles = []

searchStrings = ["check_markup", "check_plain", "check_url", "drupal_attributes", "drupal_strip_dangerous_protocols", "filter_xss", "format_string", "get_t"]
report = ''

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
#print '[*] fullPath: ', fullPath
#length = len(fullPath)

find_all_files()
#print '[*] infiles', infiles


for infile in infiles:
	#print '[debug] infile: ', infile
	with open(infile) as reviewFile:
		#print '[debug] reviewFile ', reviewFile
		for num, line in enumerate(reviewFile, 1):
			for s in searchStrings:
				if s in line:
					print '[+]', s, 'at line:', num, '\t', line.lstrip()
					report += infile + ' ' + s + ' at line: ' + str(num)  + '\n' + line.lstrip() + '\n\n'
	report += '[*] End report for ' + infile + '\n'
	report += '=== \n\n'
# ===

header = create_report_header()
fs = open('reports/' + moduleName + '-static-' + searchType + '.txt', 'w')
fs.write(header)
fs.write(report)
fs.close()
