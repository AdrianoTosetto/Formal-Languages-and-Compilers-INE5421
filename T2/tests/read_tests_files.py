import sys
sys.path.append('../')
from T2.context_free_grammar import*

'''
	This class can read from a file
'''


class ReadTestsFiles:

	def __init__(self):
		print()


	'''
		this method returns a grammar object for a given file name
	'''
	@staticmethod
	def read_file_and_get_grammar(fname):
		file = open(fname)
		return ReadTestsFiles.raw_string_to_grammar(file.read())

	'''
		helper method
	'''

	@staticmethod
	def raw_string_to_grammar(rawstr):
		productions = []
		lines = rawstr.split("\n")

		for t in lines:
			if not t:
				continue
			temp1 = t.split("->")
			temp2 = temp1[1].split("|")

			for tt in temp2:
				productions.append(Production(temp1[0].strip(' '), tt.strip(' ')))


		return Grammar(productions)


if __name__ == "__main__":
	g6 = ReadTestsFiles.read_file_and_get_grammar("g7.txt")
	print(g6)
	#g3.make_epsilon_free(set(['P','B','C','V','K']))
