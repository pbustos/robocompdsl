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
		identifier     = Word(alphas+"_",alphanums+"_")
		typeIdentifier = Word(alphas+"_",alphanums+"_:")


		## Imports
		idslImport  = Suppress(Word("import")) + quote +  CharsNotIn("\";").setResultsName('path') + quote + semicolon
		idslImports = ZeroOrMore(idslImport)


		dictionaryDef = Word("dictionary") + lt + CharsNotIn("<>;") + gt + identifier.setResultsName('name') + semicolon
		sequenceDef   = Word("sequance")   + lt + CharsNotIn("<>;") + gt + identifier.setResultsName('name') + semicolon
		enumDef       = Word("enum")       + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon
		structDef     = Word("struct")     + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon
		exceptionDef  = Word("exception")  + identifier.setResultsName('name') + op + CharsNotIn("{}") + cl + semicolon

		raiseDef       = Suppress(Word("throws")) + identifier + ZeroOrMore( Literal(',') + identifier )
		decoratorDef    = Literal('idempotent') | Literal('out')
		retValDef       = identifier.setResultsName('ret')

		firstParam    = Group( Optional(decoratorDef.setResultsName('decorator')) + typeIdentifier.setResultsName('type') + identifier.setResultsName('name'))
		nextParam     = Suppress(Word(',')) + firstParam
		params        = firstParam + ZeroOrMore(nextParam)


		remoteMethodDef  = Group(Optional(decoratorDef) + retValDef +  identifier.setResultsName('name') + opp + Optional(          params).setResultsName('params') + clp + Optional(raiseDef) + semicolon )
		interfaceDef    = Word("interface")  + identifier.setResultsName('name') + op + Group(ZeroOrMore(remoteMethodDef)) + cl + semicolon

		moduleContent = Group(structDef | enumDef | exceptionDef | dictionaryDef | sequenceDef | interfaceDef)
		module = Suppress(Word("module")) + identifier.setResultsName("name") + op + ZeroOrMore(moduleContent).setResultsName("contents") + cl + semicolon

		IDSL = idslImports.setResultsName("imports") + module.setResultsName("module")
		IDSL.ignore( cppStyleComment )


		tree = IDSL.parseString(text)

		return IDSLParsing.module(tree)

	@staticmethod
	def module(tree, start=''):
		module = {}

		#module name
		module['name'] = tree['module']['name']


		#print tree['module']['contents']
		module['interfaces'] = []
		for contentDef in tree['module']['contents']:
			if contentDef[0] == 'interface':
				interface = { 'name':contentDef[1], 'methods':{}}
				for method in contentDef[2]:
					interface['methods'][method['name']] = {}

					interface['methods'][method['name']]['name'] = method['name']
					try:
						interface['methods'][method['name']]['decorator'] = method['decorator']
					except:
						interface['methods'][method['name']]['decorator'] = ''

					interface['methods'][method['name']]['return'] = method['ret']

					params = []
					try:
						for p in method['params']:
							try:
								params.append( { 'decorator':p['decorator'], 'type':p['type'], 'name':p['name'] } )
							except:
								params.append( { 'decorator':'none',         'type':p['type'], 'name':p['name'] } )
					except:
						pass
					interface['methods'][method['name']]['params'] = params

					try:
						interface['methods'][method['name']]['throws'] = method['decorator']
					except:
						interface['methods'][method['name']]['throws'] = 'nothing'
				module['interfaces'].append(interface)
		return module

	@staticmethod
	def printModule(module, start=''):
		print 'MODULE', module['name']+':'
		print ' ', 'INTERFACES:'
		for interface in module['interfaces']:
			print '   ', interface['name']
			for mname in interface['methods']:
				method = interface['methods'][mname]
				print '     ', method['name']
				print '        decorator', method['decorator']
				print '        return', method['return']
				print '        params'
				for p in method['params']:
					print '         ', '<', p['decorator'], '>  <', p['type'], '>  <', p['name'], '>'







class IDSLPool:
	def __init__(self, files):
		self.modulePool = {}
		pathList = []
		fileList = []
		for p in [f for f in files.split('#') if len(f)>0]:
			if p.startswith("-I"):
				pathList.append(p[2:])
			else:
				fileList.append(p)
		pathList.append('/home/robocomp/robocomp/interfaces/IDSLs/')
		for f in fileList:
			filename = f.split('.')[0]
			for p in pathList:
				try:
					path = p+'/'+f
					self.modulePool[filename] = IDSLParsing.fromFile(path)
					break
				except IOError, e:
					pass
			if not filename in self.modulePool:
				print 'Couldn\'t locate ', f
				sys.exit(-1)

	def moduleProviding(self, interface):
		for module in self.modulePool:
			for m in self.modulePool[module]['interfaces']:
				if m['name'] == interface:
					return self.modulePool[module]
		return None



if __name__ == '__main__':
	idsl = IDSLParsing.fromFile(sys.argv[1])
	IDSLParsing.printModule(idsl)
