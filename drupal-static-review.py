#!/usr/bin/env python

# Imports
import sys
import yaml
from os import listdir
from os.path import isfile, join, isdir


# DrupalStaticReview class
class DrupalStaticReview:
	# constructor
	def __init__(self):
		# type: (object) -> object
		#searchType = "full"
		print "[+] Search type: %s" % searchType

	# Find all files that are part of the module
	@classmethod
	def getAllFilesRecursive():
		files = [join(codeDirectory, f) for f in listdir(codeDirectory) if isfile(join(codeDirectory, f))]
		dirs = [d for d in listdir(codeDirectory) if isdir(join(codeDirectory, d))]
		for d in dirs:
			files_in_d = getAllFilesRecursive(join(codeDirectory, d))
			if files_in_d:
				for f in files_in_d:
					files.append(join(codeDirectory, f))
		return files

	# Iterate over each file that is part of the module
	@classmethod
	def searchFile(cls):
		print "[+] Searching file: %s" % sfile


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

print "[*] Performing %s search on %s" % (searchType, moduleName)
print "[*]  located in %s" % codeDirectory

review = DrupalStaticReview()


