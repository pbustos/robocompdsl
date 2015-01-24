#!/usr/bin/env python



import sys, os

files = [ 'main.cpp' ]

inputFile  = sys.argv[1]
outputPath = sys.argv[2]

try:
	os.mkdir(outputPath)
except:
	pass


for f in files:
	os.system("cog.py -z -d -D thefile=" + inputFile + " -o " + outputPath + '/' + f + " templateCPP/" + f)


