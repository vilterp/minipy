class FileOfCode:
	def __init__(self, defs):
		self.defs = defs

class Expression:
	pass

class Ident(Expression):
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return self.name

class IfExpr(Expression):
	def __init__(self, cond, ifBlock, elseBlock):
		self.cond = cond
		self.ifBlock = ifBlock
		self.elseBlock = elseBlock
	def __repr__(self):
		return 'if {0} then {1} else {2}'.format(self.cond, self.ifBlock, self.elseBlock)

class FuncCall(Expression):
	def __init__(self, func, args):
		self.func = func
		self.args = args
	def __repr__(self):
		return '{0}({1})'.format(self.func, ','.join(map(repr, self.args)))

class FuncDef:
	def __init__(self, ident, args, block):
		self.ident = ident
		self.args = args
		self.block = block
	def __repr__(self):
		# return 'def {0}({1})'.format(self.ident, self.args, '\n'.join())
		return 'def {0}({1}) {{\n{2}\n}}'.format(repr(self.ident), self.args, '\n'.join(map(repr, self.block)))

class Statement:
	pass

class ReturnStmt(Statement):
	def __init__(self, expr):
		self.expr = expr
	def __repr__(self):
		return 'return {0}'.format(self.expr)

class Assignment(Statement):
	def __init__(self, ident, expr):
		self.ident = ident
		self.expr = expr
	def __repr__(self):
		return '{0} = {1}'.format(self.ident, self.expr)

class GoStmt(Statement):
	def __init__(self, funcCall):
		self.funcCall = funcCall
