import sys
import pyparsing

import parser
import interpret

def run_file(path):
	try:
		parsed = parser.fileOfCode.parseFile(path)[0]
		interpret.call_fun(parsed.defs, 'main', sys.argv[2:])
	except pyparsing.ParseException, e:
		print 'Parse Error:', e

def run_string(code, *args):
	parsed = parser.fileOfCode.parseString(code)
	interpret.call_fun(parsed.defs, 'main', args)

if __name__ == '__main__':
	path = sys.argv[1]
	run_file(path)
