
from context_free_grammar import *

class ReadTestsFiles:

	def __init__(self):
		print()

	@staticmethod
	def read_file_and_get_grammar(fname):
		file = open(fname)
		return ReadTestsFiles.raw_string_to_grammar(file.read())
	@staticmethod
	def raw_string_to_grammar(rawstr):
		productions = []
		temp = rawstr.split("\n")

		for t in temp:
			temp1 = t.split("->")
			temp2 = temp1[1].split("|")

			for tt in temp2:
				productions.append(Production(temp1[0], tt))

		#print(temp)

		g = Grammar(productions)
		print(g)
		return None