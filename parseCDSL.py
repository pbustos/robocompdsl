#!/usr/bin/env python

from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr

import sys

debug = False
#debug = True


class CDSLParsing:
	@staticmethod
	def fromFile(filename, verbose=False, includeIncludes=True):
		# Open input file
		inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('//')])
		return CDSLParsing.fromString(inputText)
	@staticmethod
	def fromString(inputText, verbose=False):
		if verbose: print 'Verbose:', verbose
		text = nestedExpr("/*", "*/").suppress().transformString(inputText) 

		semicolon = Suppress(Word(";"))
		quote     = Suppress(Word("\""))
		op        = Suppress(Word("{"))
		cl        = Suppress(Word("}"))
		opp       = Suppress(Word("("))
		clp       = Suppress(Word(")"))
		identifier = Word( alphas+"_", alphanums+"_" )
		
		# Imports
		idslImport  = Suppress(Word("import")) + quote +  CharsNotIn("\";").setResultsName('path') + quote + semicolon
		idslImports = OneOrMore(idslImport)
		# Communications
		implementsList = Group(Word('implements')    + identifier + ZeroOrMore(Suppress(Word(',')) + identifier) + semicolon)
		requiresList   = Group(Word('requires')      + identifier + ZeroOrMore(Suppress(Word(',')) + identifier) + semicolon)
		subscribesList = Group(Word('subscribesTo')  + identifier + ZeroOrMore(Suppress(Word(',')) + identifier) + semicolon)
		publishesList  = Group(Word('publishesList') + identifier + ZeroOrMore(Suppress(Word(',')) + identifier) + semicolon)
		communicationList = implementsList | requiresList | subscribesList | publishesList
		communications = Group( Suppress(Word("Communications")) + op + ZeroOrMore(communicationList) + cl + semicolon)
		# Language
		language = Suppress(Word("language")) + (Word("Cpp")|Word("Python")) + semicolon
		# GUI
		gui = Optional(Group( Word("gui") + Word("Qt") + opp + identifier + clp + semicolon ))
		
		componentContents = communications.setResultsName('communications') & language.setResultsName('language') & gui.setResultsName('gui')
		component = Suppress(Word("Component")) + identifier.setResultsName("name") + op + componentContents.setResultsName("properties") + cl + semicolon		

		CDSL = idslImports.setResultsName("imports") + component.setResultsName("component")
		tree = CDSL.parseString(text)


		CDSLParsing.printComponent(tree)

	@staticmethod
	def printComponent(tree, start=''):
		# Component name
		print 'Component', tree['component']['name']
		# Imports
		print '\tImports:'
		for imp in tree['imports']:
			print '\t\t', imp
		# Language
		print '\tLanguage:'
		print '\t\t',tree['properties']['language'][0]
		# GUI
		print '\tGUI:'
		gui = 'No GUI'
		try:
			gui = tree['properties']['gui'][0]
		except:
			pass
		print '\t\t', gui
		# Communications
		print '\tCommunications:'
		implementsList = []
		requiresList   = []
		subscribesList = []
		publishesList  = []
		for comm in tree['properties']['communications']:
			if comm[0] == 'implements':
				for interface in comm[1:]: implementsList.append(interface)
			if comm[0] == 'requires':
				for interface in comm[1:]: requiresList.append(interface)
			if comm[0] == 'publishes':
				for interface in comm[1:]: publishesList.append(interface)
			if comm[0] == 'subscribesTo':
				for interface in comm[1:]: subscribesList.append(interface)
		print '\t\tImplements', implementsList
		print '\t\tRequires', requiresList
		print '\t\tPublishes', implementsList
		print '\t\tSubscribes', subscribesList

			

CDSLParsing.fromFile(sys.argv[1])