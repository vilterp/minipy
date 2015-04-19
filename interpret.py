from __future__ import print_function
import operator as op

from mpast import *

BUILTINS = {
	'print': print,
    'or': op.or_,
    'plus': op.add,
    'minus': op.sub,
    'eq': op.eq
}

class CodeError(Exception):
	pass

class Interpreter:

	def __init__(self, defs):
		self.defs = {}
		for func_def in defs:
			self.defs[func_def.ident.name] = func_def
		self.stack = []

	def call(self, func_name, args):
		if BUILTINS.has_key(func_name):
			return BUILTINS[func_name](*args)
		if self.defs.has_key(func_name):
			func_def = self.defs[func_name]
		else:
			raise CodeError('{0} not found'.format(func_name))
		sf = StackFrame(func_name)
		if not len(args) == len(func_def.args):
			raise CodeError('{0} needs {1} args; got {2}'.format(func_name, len(func_def.args), len(args)))
		else:
			for i in range(len(func_def.args)):
				ident = func_def.args[i]
				sf.scope[ident.name] = args[i]
		self.stack.append(sf)
		retval = self.run_block(func_def.block)
		self.stack.pop()
		return retval

	def run_block(self, block):
		sf = self.stack[-1]
		for s_or_e in block:
			if isinstance(s_or_e, Expression):
				expr = s_or_e
				self.evaluate(expr)
			elif isinstance(s_or_e, Statement):
				stmt = s_or_e
				if isinstance(stmt, ReturnStmt):
					return self.evaluate(stmt.expr)
				elif isinstance(stmt, Assignment):
					sf.scope[stmt.ident.name] = self.evaluate(stmt.expr)

	def evaluate(self, expr):
		sf = self.stack[-1]
		# functions as values?
		if isinstance(expr, list): # block
			self.run_block(expr)
		elif isinstance(expr, Ident):
			return sf.scope[expr.name]
		elif isinstance(expr, IfExpr):
			if self.evaluate(expr.cond) is True:
				return self.evaluate(expr.ifBlock)
			else:
				return self.evaluate(expr.elseBlock)
		elif isinstance(expr, FuncCall):
			args = map(self.evaluate, expr.args)
			retval = self.call(expr.func.name, args)
			return retval
		elif isinstance(expr, str):
			return expr
		elif isinstance(expr, int):
			return expr


class StackFrame:

	def __init__(self, func_name):
		self.scope = {}
		self.func_name = func_name

def call_fun(defs, name, args):
	interp = Interpreter(defs)
	try:
		interp.call(name, args)
	except CodeError, e:
		print('Code Error (TODO: tracebacks):', e)