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
	def fromString(inputText, verbose=False, includeIncludes=True):
		if verbose: print 'Verbose:', verbose

		text = nestedExpr("/*", "*/").suppress().transformString(inputText) 

		semicolon = Suppress(Word(";"))
		quote     = Suppress(Word("\""))
		op        = Suppress(Word("{"))
		cl        = Suppress(Word("}"))

		variable = Word(srange("[a-zA-Z_]"))
		
		idslImport  = Word("import") + quote +  CharsNotIn("\"") + quote + semicolon
		idslImports = OneOrMore(idslImport)

		communications = Word("Communications") + op + ZeroOrMore() + cl + semicolon
		
		language = ( Word("language") + (Word("Cpp")|Word("Python")) + semicolon

		gui = Optional( Word("gui") + Word("Qt") + semicolon )

		componentContents = communications & language & gui
		component = Word("Component") + op +`componentContents + cl + semicolon
		
		CDSL = idslImports + component

		## Define AGM's DSL meta-model
		#an = Word(srange("[a-zA-Z0-9_.]"))
		#ids = Word(srange("[a-zA-Z0-9_]"))
		#almostanything = CharsNotIn("{}")
		#incPath = CharsNotIn("()")
		#parameters = Suppress("parameters")
		#precondition = Suppress("precondition")
		#effect = Suppress("effect")
		#plusorminus = Literal('+') | Literal('-')
		#number = Word(nums)
		#nu = Combine( Optional(plusorminus) + number )
		#neg = Optional(Literal('*'))
		#sep = Suppress("===")
		#eq = Suppress("=")
		#cn = Suppress(":")
		#lk = Suppress("->")
		#ar = Suppress("=>")
		#op = Suppress("{")
		#cl = Suppress("}")
		#po = Suppress("(")
		#co = Suppress(",")
		#pt = Suppress(".")
		#pc = Suppress(")")
		#no = Suppress("!")

		## LINK
		#link  = Group(an.setResultsName("lhs") + lk + an.setResultsName("rhs") + po + Optional(no).setResultsName("no") + an.setResultsName("linkType") + pc + neg.setResultsName("enabled"))
		## NODE
		#node  = Group(an.setResultsName("symbol") + cn + an.setResultsName("symbolType") + Optional(po + nu.setResultsName("x") + co + nu.setResultsName("y") + pc))
		## GRAPH
		#graph = Group(op + ZeroOrMore(node).setResultsName("nodes") + ZeroOrMore(link).setResultsName("links") + cl)
		## COMBO RULE
		#atom = Group(ids.setResultsName("name") + Suppress("as") + ids.setResultsName("alias") + Optional("optional"))
		#equivElement = Group(ids.setResultsName("rule") + pt + ids.setResultsName("variable"))
		#equivRhs = eq + equivElement
		#equiv = Group(equivElement.setResultsName("first") + OneOrMore(equivRhs).setResultsName("more"))
		#rule_seq  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + OneOrMore(atom).setResultsName("atomss") + Suppress("where:") + ZeroOrMore(equiv).setResultsName("equivalences") + cl)
		## NORMAL RULE
		#Prm = Optional(parameters   + op + almostanything + cl).setResultsName("parameters")
		#Cnd = Optional(precondition + op + almostanything + cl).setResultsName("precondition")
		#Eft = Optional(effect       + op + almostanything + cl).setResultsName("effect")
		#rule_nrm = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + Prm + Cnd + Eft + cl)
		## HIERARCHICAL RULE
		#rule_hierarchical = Group(Literal("hierarchical").setResultsName("hierarchical") + an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + Prm + Cnd + Eft + cl)
		## indlude
		#include = Group(Suppress("include") + po + incPath.setResultsName("includefile") + pc)
		## GENERAL RULE
		#rule = rule_nrm | rule_seq | rule_hierarchical | include
		## PROPERTY
		#prop  = Group(an.setResultsName("prop") + eq + an.setResultsName("value"))
		## WHOLE FILE
		#agm   = OneOrMore(prop).setResultsName("props") + sep + OneOrMore(rule).setResultsName("rules") + StringEnd()

		#agm.parseWithTabs().parseString(inputText)

		


CDSLParsing.fromFile(sys.argv[1])