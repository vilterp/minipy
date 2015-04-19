import pyparsing as pp
from pyparsing import *
from mpast import *

funcDef = Forward()

fileOfCode = OneOrMore(funcDef).setParseAction(lambda toks: FileOfCode(toks))

identifier = Word(alphas).setParseAction(lambda toks: Ident(*toks)).setName('Ident')

integer = Word(nums).setParseAction(lambda toks: int(*toks))

string = QuotedString('"')

true = Keyword('True').setParseAction(lambda toks: True)

false = Keyword('False').setParseAction(lambda toks: False)

expression = Forward()

parenExpr = Literal('(').suppress() + expression + Literal(')').suppress()

ifExpr = (Keyword('if').suppress() + expression + Keyword('then').suppress() + expression + Keyword('else').suppress() + expression).setParseAction(lambda toks: IfExpr(*toks))

listLiteral = Literal('[').suppress() + Optional(delimitedList(expression), default=[]) + Literal(']').suppress()

funcCall = Forward()
block = Forward()

expression << pp.Or([ifExpr, true, false, identifier, integer, string, parenExpr, funcCall, block, listLiteral])

args = Group(Optional(delimitedList(expression), default=[]))

funcCall << (identifier + '(' + args + ')').setParseAction(lambda toks: FuncCall(toks[0], toks[2]))

funcDef << (Keyword('def') + identifier + '(' + Optional(Group(delimitedList(identifier)), default=[]) + ')' + block).setParseAction(lambda toks: FuncDef(toks[1], toks[3], toks[5]))

returnStmt = (Keyword('return') + expression).setParseAction(lambda toks: ReturnStmt(toks[1]))

assignment = (identifier + '=' + expression).setParseAction(lambda toks: Assignment(toks[0], toks[2]))

forLoop = Keyword('for') + identifier + Keyword('in') + expression + block

statement = pp.Or([returnStmt, assignment, forLoop])

block << Literal('{').suppress() + Group(OneOrMore(pp.Or([statement, expression]))) + Literal('}').suppress()
