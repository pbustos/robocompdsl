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
		#inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('//')])
		inputText = "\n".join([line for line in open(filename, 'r').read().split("\n")])
		return IDSLParsing.fromString(inputText)
	@staticmethod
	def fromString(inputText, verbose=False):
		if verbose: print 'Verbose:', verbose
		#text = nestedExpr("/*", "*/").suppress().transformString(inputText) 
		text = inputText

		semicolon = Suppress(Word(";"))
		quote     = Suppress(Word("\""))
		op        = Suppress(Word("{"))
		cl        = Suppress(Word("}"))
		opp       = Suppress(Word("("))
		clp       = Suppress(Word(")"))
		lt       = Suppress(Word("<"))
		gt       = Suppress(Word(">"))
		identifier = Word( alphas+"_", alphanums+"_" )
		
		## Imports
		idslImport  = Suppress(Word("import")) + quote +  CharsNotIn("\";").setResultsName('path') + quote + semicolon
		idslImports = ZeroOrMore(idslImport)


		dictionaryDef = Word("dictionary") + lt + CharsNotIn("<>;") + gt + identifier.setResultsName('name') + semicolon
		sequenceDef   = Word("sequance")   + lt + CharsNotIn("<>;") + gt + identifier.setResultsName('name') + semicolon
		enumDef       = Word("enum")       + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon
		structDef     = Word("struct")     + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon
		exceptionDef  = Word("exception")  + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon
		
		raiseDef       = Optional(Suppress(Word("throws")) + identifier)
		decoratorDef    = Optional( (Word('idempotent') | Word('out') | Word('idempotent')).setResultsName('dec') )
		retValDef       = identifier.setResultsName('ret')

		param         = Group( Optional(decoratorDef.setResultsName('decorator')) + identifier.setResultsName('type') + identifier.setResultsName('name'))
		params        = param        +  ZeroOrMore(Suppress(Word(',')) + param)

		remoteMethodDef = Group(decoratorDef + retValDef +  identifier.setResultsName('name') + opp + Optional(params).setResultsName('params') + clp + raiseDef + semicolon )
		#remoteMethodDef = Group( ++ + semicolon )
		interfaceDef    = Word("interface")  + identifier.setResultsName('name') + op + Group(ZeroOrMore(remoteMethodDef)) + cl + semicolon

		moduleContent = Group(structDef | enumDef | exceptionDef | dictionaryDef | sequenceDef | interfaceDef)
		module = Suppress(Word("module")) + identifier.setResultsName("name") + op + ZeroOrMore(moduleContent).setResultsName("contents") + cl + semicolon		

		IDSL = idslImports.setResultsName("imports") + module.setResultsName("module")
		IDSL.ignore( cppStyleComment )
		tree = IDSL.parseString(text)


		return IDSLParsing.module(tree)

	@staticmethod
	def printmodule(module, start=''):
		# module name
		print 'module', module['name']
		# Imports
		## Language
		#print '\tLanguage:'
		#print '\t\t', module['language']
		## GUI
		#print '\tGUI:'
		#print '\t\t', module['gui']
		## Communications
		#print '\tCommunications:'
		#print '\t\tImplements', module['implements']
		#print '\t\tRequires', module['requires']
		#print '\t\tPublishes', module['publishes']
		#print '\t\tSubscribes', module['subscribesTo']

	@staticmethod
	def module(tree, start=''):
		module = {}
		
		# module name
		module['name'] = tree['module']['name']


		#print tree['module']['contents']
		module['interfaces'] = []
		for contentDef in tree['module']['contents']:
			if contentDef[0] == 'interface':
				print 'INTERFACE', contentDef[1]
				
				for method in contentDef[2]:

					print '\t', method['name']

					print '\t\tDecorator: ', 
					try:
						print method['decorator']
					except:
						print ''

					print '\t\tReturn value: ', method['ret']

					print '\t\tParams:',
					try:
						print method['params']
					except:
						print ''

					print '\t\tThrows:',
					try:
						print method['throws']
					except:
						print ''




		## Imports
		#module['imports'] = []
		#for imp in tree['imports']:
			#module['imports'] .append(imp)
		## Language
		#module['language'] = tree['contents']['language'][0]
		## GUI
		#module['gui'] = 'none'
		#try:
			#module['gui'] = tree['gui'][0]
		#except:
			#pass

		## Communications
		#module['implements']   = []
		#module['requires']     = []
		#module['publishes']    = []
		#module['subscribesTo'] = []
		#for comm in tree['contents']['communications']:
			#if comm[0] == 'implements':
				#for interface in comm[1:]: module['implements'].append(interface)
			#if comm[0] == 'requires':
				#for interface in comm[1:]: module['requires'].append(interface)
			#if comm[0] == 'publishes':
				#for interface in comm[1:]: module['publishes'].append(interface)
			#if comm[0] == 'subscribesTo':
				#for interface in comm[1:]: module['subscribesTo'].append(interface)
		return module

if __name__ == '__main__':
	idsl = IDSLParsing.fromFile(sys.argv[1])
	IDSLParsing.printmodule(idsl)
	