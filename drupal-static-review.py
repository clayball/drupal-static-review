#!/usr/bin/env python

# Imports
import sys
import yaml
import mmap
from os import listdir
from os.path import isfile, join, isdir


# DrupalStaticReview class
class DrupalStaticReview:
	# constructor
	def __init__(self):
		# type: (object) -> object
		print "[*] Search type: %s" % searchType

	# Find all files that are part of the module
	@classmethod
	def get_all_files(self, fullPath):
		files = [join(fullPath, f) for f in listdir(fullPath) if isfile(join(fullPath, f))]
		dirs = [d for d in listdir(fullPath) if isdir(join(fullPath, d))]
		for d in dirs:
			files_in_d = self.get_all_files(join(fullPath, d))
			if files_in_d:
				for f in files_in_d:
					files.append(join(fullPath, f))
		new_fileList = []
		for file in files:
			tempFile = file
			for filetype in fileTypes:
				if file.split('.', -1)[-1] == filetype:
					new_fileList += [file]
		#print '[+] new_fileList: %s' % new_fileList
		return new_fileList

	# Iterate over each file that is part of the module
	@classmethod
	def search_file(self):
		string_found = 0
		root_item = items
		root_item = root_item.split('/', -1)[-1]
		report_content = ''
		for queries in searchStrings:
			is_bad = 0
			if debugMessages == True:
				print '[+] queries: %s' % queries
			if s.find(queries) != -1:
				if debugMessages == True:
					print '[+] queries != -1: %s' % queries
				report_content = '\n'
				report_content += '= File: ' + root_item + '\n'
				report_content += '========================================\n\n'
				module_status = 'Found: ' + queries
				module_path = ' in ' + items[length:] + '\n\n'
				report_content += module_status + module_path
				string_found = 1
		return report_content

	# Write report header
	@classmethod
	def create_report_header(self):
		report_header =  'Static Report for ' + moduleName + '\n'
		report_header += 'Search type: ' + searchType + '\n'
		report_header += '==================================================\n\n'
		if debugMessages == True:
			print '\n\n' + report_header
		return report_header


# Main section

# get arguments
moduleName = sys.argv[1]
# TODO: sanitize/validate/encode? input

# Allow search for specific types of strings, e.g. sqli_strings, or allif len(sys.argv[2]):
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

review = DrupalStaticReview()
fullPath = codeDirectory + '/' + moduleName
length = len(fullPath)
reviewFiles = review.get_all_files(fullPath)

print '[*] reviewFiles: %s' % reviewFiles

content = ''
for items in reviewFiles:
	f = open(items)
	s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
	content += review.search_file()
fs = open('reports/' + moduleName + '-static-' + searchType + '.txt', 'w')
report_head = review.create_report_header()
fs.write(report_head)
fs.write(content)
fs.close()
print content
