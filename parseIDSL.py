#!/usr/bin/env python

from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr

import sys

debug = False
#debug = True


class IDSLParsing:
	@staticmethod
	def fromFile(filename, verbose=False, includeIncludes=True):
		# Open input file
		inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('//')])
		return IDSLParsing.fromString(inputText)
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
		
		moduleContents = communications.setResultsName('communications') & language.setResultsName('language') & gui.setResultsName('gui')
		module = Suppress(Word("module")) + identifier.setResultsName("name") + op + moduleContents.setResultsName("properties") + cl + semicolon		

		IDSL = idslImports.setResultsName("imports") + module.setResultsName("module")
		tree = IDSL.parseString(text)


		return IDSLParsing.module(tree)

	@staticmethod
	def printmodule(module, start=''):
		# module name
		print 'module', module['name']
		# Imports
		print '\tImports:'
		for imp in module['imports']:
			print '\t\t', imp
		# Language
		print '\tLanguage:'
		print '\t\t', module['language']
		# GUI
		print '\tGUI:'
		print '\t\t', module['gui']
		# Communications
		print '\tCommunications:'
		print '\t\tImplements', module['implements']
		print '\t\tRequires', module['requires']
		print '\t\tPublishes', module['publishes']
		print '\t\tSubscribes', module['subscribesTo']

	@staticmethod
	def module(tree, start=''):
		module = {}
		
		# module name
		module['name'] = tree['module']['name']
		# Imports
		module['imports'] = []
		for imp in tree['imports']:
			module['imports'] .append(imp)
		# Language
		module['language'] = tree['properties']['language'][0]
		# GUI
		module['gui'] = 'none'
		try:
			module['gui'] = tree['gui'][0]
		except:
			pass

		# Communications
		module['implements']   = []
		module['requires']     = []
		module['publishes']    = []
		module['subscribesTo'] = []
		for comm in tree['properties']['communications']:
			if comm[0] == 'implements':
				for interface in comm[1:]: module['implements'].append(interface)
			if comm[0] == 'requires':
				for interface in comm[1:]: module['requires'].append(interface)
			if comm[0] == 'publishes':
				for interface in comm[1:]: module['publishes'].append(interface)
			if comm[0] == 'subscribesTo':
				for interface in comm[1:]: module['subscribesTo'].append(interface)
		return module

if __name__ == '__main__':
	IDSLParsing.fromFile(sys.argv[1])
