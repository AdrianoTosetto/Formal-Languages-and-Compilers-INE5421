import sys
sys.path.append('../')
from context_free_grammar import*

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
	def raw_string_to_grammar(rawstr, name=None):
		productions = []
		lines = rawstr.split("\n")

		for t in lines:
			if not t:
				continue
			temp1 = t.split("->")
			temp2 = temp1[1].split("|")

			for tt in temp2:
				productions.append(Production(temp1[0].strip(' '), tt.strip(' ')))


		return Grammar(productions, name)


class FileParser:

	@staticmethod
	def get_grammars_from_file(filename):
		grammars_obj = []
		file = open(filename)
		rawstr = file.read()

		rawgrammars = rawstr.split("new_grammar")
		rawgrammars = rawgrammars[1:len(rawgrammars)]
		for rawgrammar in rawgrammars:
			rawgrammar = ''.join((rawgrammar.strip(), '\n'))
			rawgrammar_temp1 = rawgrammar.split('\n', 1)
			#print(rawgrammar_temp1[0])
			grammars_obj.append(ReadTestsFiles.raw_string_to_grammar(rawgrammar_temp1[1], rawgrammar_temp1[0]))
		return grammars_obj
	@staticmethod
	def save_grammars_to_file(filename, grammars):
		open(filename, 'w').close()
		f = open(filename, "+a")
		for grammar in grammars:
			str_grammar = str(grammar)
			str_grammar = ("\nnew_grammar\n"+grammar.name+":\n" + str_grammar).strip() + '\n'
			f.write(str_grammar)
if __name__ == "__main__":
	p = FileParser()
	#print(p.get_grammars_from_file("../teste_save.txt")[0])
	gs = p.get_grammars_from_file("../teste_save.txt")
	print(gs[0])
	print(gs[1])
	print("=============")
	p.save_grammars_to_file('sd.txt', gs)
	gs = p.get_grammars_from_file("sd.txt")
	print(gs[0])
	print(gs[1])
	#g6 = ReadTestsFiles.read_file_and_get_grammar("g7.txt")
	#print(g6)
	#g3.make_epsilon_free(set(['P','B','C','V','K']))
