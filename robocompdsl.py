#!/usr/bin/env python


# main.cpp

# SERVANTS
#CMakeLists.txt
#commonbehaviorI.h
#genericmonitor.cpp
#genericworker.cpp
#specificmonitor.h
#specificworker.h
#CMakeListsSpecific.txt
#commonbehaviorI.cpp
#config.h
#genericmonitor.h
#genericworker.h
#specificmonitor.cpp
#specificworker.cpp

import sys, os

# Read input CDSL file
inputFile  = sys.argv[1]
from parseCDSL import *
component = CDSLParsing.fromFile(inputFile)


# Check output directory
outputPath = sys.argv[2]
try:
	os.mkdir(outputPath)
except:
	pass


#
# Misc functions
#
def replaceTagsInFile(path):
	i = open(path, 'r')
	text = i.read()
	reps = []
	reps.append(["\n<@@<" ,""])
	reps.append([">@@>\n" ,""])
	reps.append(["<TABHERE>", '\t'])
	reps.append(["<S1>", ' '])
	reps.append(["<S2>", '  '])
	reps.append(["<S4>", '    '])
	for r in reps:
		text = text.replace(r[0], r[1])
	i.close()
	w = open(path, 'w')
	w.write(text)
	w.close()


#
# Generate regular files
#
files = [ 'CMakeLists.txt', 'src/main.cpp', 'src/CMakeLists.txt', 'src/CMakeListsSpecific.txt' ]
for f in files:
	ofile = outputPath + '/' + f
	print 'Generating', ofile
	os.system("cog.py -z -d -D thefile=" + inputFile + " -o " + ofile + " templateCPP/" + f)
	replaceTagsInFile(outputPath + '/' + f)


#
# Generate interface-dependent files
#
for im in component['implements']:
	for f in [ "SERVANT.H", "SERVANT.CPP"]:
		ofile = outputPath + '/' + im.lower() + 'I.' + f.split('.')[-1].lower()
		print 'Generating', ofile, ' (servant for', im + ')'
		# Call cog
		os.system("cog.py -z -d -D thefile=" + inputFile + " -o " + ofile + " templateCPP/" + f)
		replaceTagsInFile(ofile)



		#w = IMPLEMENTS_STR.replace("<NORMAL>", im).replace("<LOWER>", im.lower())
		#cog.outl(w)

#for st in component['subscribesTo']:
	#w = SUBSCRIBESTO_STR.replace("<NORMAL>", st).replace("<LOWER>", st.lower())
	#cog.out(w)
