#!/usr/bin/env python


# TODO
#
# Read ports from component-ports.txt for the files in etc.
#
#

import sys, os, subprocess

# Read input CDSL file
inputFile  = sys.argv[1]
from parseCDSL import *
component = CDSLParsing.fromFile(inputFile)


# Check output directory
outputPath = sys.argv[2]

if os.path.exists(outputPath):
	print 'can\'t create ', outputPath, 'directory'
	sys.exit(1)

try:
	os.mkdir(outputPath)
	os.mkdir(outputPath+"/bin")
	os.mkdir(outputPath+"/etc")
	os.mkdir(outputPath+"/src")
except:
	print 'there was a problem creating a directory'
	sys.exit(1)
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


#genericworker.cpp
#specificworker.h
#specificworker.cpp

#
# Generate regular files
#
files = [ 'CMakeLists.txt', 'DoxyFile', 'README-STORM.txt', 'etc/config', 'src/main.cpp', 'src/CMakeLists.txt', 'src/CMakeListsSpecific.txt', 'src/commonbehaviorI.h', 'src/commonbehaviorI.cpp', 'src/genericmonitor.h', 'src/genericmonitor.cpp', 'src/config.h', 'src/specificmonitor.h', 'src/specificmonitor.cpp', 'src/genericworker.h' ]
for f in files:
	ofile = outputPath + '/' + f
	ifile = "templateCPP/" + f
	print 'Generating', ofile, 'from', ifile
	run = "cog.py -z -d -D thefile=" + inputFile + " -o " + ofile + " " + ifile
	run = run.split(' ')
	ret = subprocess.check_call(run)
	if ret != 0:
		print 'ERROR'
		sys.exyt(-1)
	replaceTagsInFile(outputPath + '/' + f)


#
# Generate interface-dependent files
#
imports = ''.join( [ imp.split('/')[-1]+'#' for imp in component['imports'] ] )
print imports
for im in component['implements']:
	for f in [ "SERVANT.H", "SERVANT.CPP"]:
		ofile = outputPath + '/src/' + im.lower() + 'I.' + f.split('.')[-1].lower()
		print 'Generating', ofile, ' (servant for', im + ')'
		# Call cog
		run = "cog.py -z -d -D theCDSL="+inputFile  + " -D theIDSLs="+imports + " -D theInterface="+im + " -o " + ofile + " " + "templateCPP/" + f
		run = run.split(' ')
		ret = subprocess.check_call(run)
		if ret != 0:
			print 'ERROR'
			sys.exyt(-1)
		replaceTagsInFile(ofile)



		#w = IMPLEMENTS_STR.replace("<NORMAL>", im).replace("<LOWER>", im.lower())
		#cog.outl(w)

#for st in component['subscribesTo']:
	#w = SUBSCRIBESTO_STR.replace("<NORMAL>", st).replace("<LOWER>", st.lower())
	#cog.out(w)
