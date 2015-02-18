#!/usr/bin/env python


# TODO
#
# Read ports from component-ports.txt for the files in etc.
#
#

import sys, os, subprocess

if len(sys.argv) < 3:
	print 'Usage:\n\t'+sys.argv[0]+'   INPUT_FILE.CDSL   OUTPUT_DIRECTORY'
	sys.exit(-1)
inputFile  = sys.argv[1]
outputPath = sys.argv[2]


from parseCDSL import *
component = CDSLParsing.fromFile(inputFile)

#########################################
# Directory structure and other checks  #
#########################################
# Function to create directories
def creaDirectorio(directory):
	try:
		print 'Creating', directory,
		os.mkdir(directory)
		print ''
	except:
		if os.path.isdir(directory):
			print '(already existed)'
			pass
		else:
			print '\nCOULDN\'T CREATE', directory
			sys.exit(-1)


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



imports = ''.join( [ imp.split('/')[-1]+'#' for imp in component['imports'] ] )

if component['language'].lower() == 'cpp':
	#
	# Check output directory
	#
	if not os.path.exists(outputPath):
		creaDirectorio(outputPath)
	# Create directories within the output directory
	try:
		creaDirectorio(outputPath+"/bin")
		creaDirectorio(outputPath+"/etc")
		creaDirectorio(outputPath+"/src")
	except:
		print 'There was a problem creating a directory'
		sys.exit(1)
		pass
	#
	# Generate regular files
	#
	files = [ 'CMakeLists.txt', 'DoxyFile', 'README-STORM.txt', 'etc/config', 'src/main.cpp', 'src/CMakeLists.txt', 'src/CMakeListsSpecific.txt', 'src/commonbehaviorI.h', 'src/commonbehaviorI.cpp', 'src/genericmonitor.h', 'src/genericmonitor.cpp', 'src/config.h', 'src/specificmonitor.h', 'src/specificmonitor.cpp', 'src/genericworker.h', 'src/genericworker.cpp', 'src/specificworker.h', 'src/specificworker.cpp', 'src/specificmonitor.h', 'src/specificmonitor.cpp' ]
	specificFiles = [ 'src/specificworker.h', 'src/specificworker.cpp', 'src/CMakeListsSpecific.txt' ]
	for f in files:
		ofile = outputPath + '/' + f
		if f in specificFiles and os.path.exists(ofile):
			print 'Skipping overwriting specific file:', ofile
			continue
		ifile = "templateCPP/" + f
		print 'Generating', ofile, 'from', ifile
		run = "cog.py -z -d -D theCDSL="+inputFile + " -D theIDSLs="+imports + " -o " + ofile + " " + ifile
		print run
		run = run.split(' ')
		ret = subprocess.check_call(run)
		if ret != 0:
			print 'ERROR'
			sys.exyt(-1)
		replaceTagsInFile(outputPath + '/' + f)
	#
	# Generate interface-dependent files
	#
	for im in component['implements']+component['subscribesTo']:
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
elif component['language'].lower() == 'python':
	#
	# Check output directory
	#
	if not os.path.exists(outputPath):
		creaDirectorio(outputPath)
	# Create directories within the output directory
	try:
		creaDirectorio(outputPath+"/etc")
		creaDirectorio(outputPath+"/src")
	except:
		print 'There was a problem creating a directory'
		sys.exit(1)
		pass
	#
	# Generate regular files
	#
	files = [ 'CMakeLists.txt', 'DoxyFile', 'README-STORM.txt', 'etc/config', 'src/main.py', 'src/commonbehaviorI.py', 'src/genericmonitor.py', 'src/specificmonitor.py', 'src/genericworker.py', 'src/specificworker.py', 'src/specificmonitor.py' ]
	specificFiles = [ 'src/specificworker.py' ]
	for f in files:
		ofile = outputPath + '/' + f
		if f in specificFiles and os.path.exists(ofile):
			print 'Skipping overwriting specific file:', ofile
			continue
		ifile = "templatePython/" + f
		print 'Generating', ofile, 'from', ifile
		run = "cog.py -z -d -D theCDSL="+inputFile + " -D theIDSLs="+imports + " -o " + ofile + " " + ifile
		run = run.split(' ')
		ret = subprocess.check_call(run)
		if ret != 0:
			print 'ERROR'
			sys.exyt(-1)
		replaceTagsInFile(outputPath + '/' + f)
	#
	# Generate interface-dependent files
	#
	for im in component['implements']+component['subscribesTo']:
		for f in [ "SERVANT.PY"]:
			ofile = outputPath + '/src/' + im.lower() + 'I.' + f.split('.')[-1].lower()
			print 'Generating', ofile, ' (servant for', im + ')'
			# Call cog
			run = "cog.py -z -d -D theCDSL="+inputFile  + " -D theIDSLs="+imports + " -D theInterface="+im + " -o " + ofile + " " + "templatePython/" + f
			run = run.split(' ')
			ret = subprocess.check_call(run)
			if ret != 0:
				print 'ERROR'
				sys.exyt(-1)
			replaceTagsInFile(ofile)
else:
	print 'Unsupported language', component['language']




