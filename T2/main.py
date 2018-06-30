'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

from context_free_grammar import *
import sys
sys.path.append('tests/')
from read_tests_files import *


if __name__ == "__main__":
	#g4 = ReadTestsFiles.read_file_and_get_grammar("g4.txt")
	#g5 = ReadTestsFiles.read_file_and_get_grammar("g5.txt")
	#g4.remove_left_recursion()
	#g5.remove_left_recursion()
	'''g7 = ReadTestsFiles.read_file_and_get_grammar("g7.txt")
	print(g7)
	print(g7.get_NA('B', set()))

	g5 = ReadTestsFiles.read_file_and_get_grammar("g5.txt")
	print(g5)
	print(g5.get_NA('T'))
	print(g5)
	print(g5.get_NA('P'))'''

	g8 = ReadTestsFiles.read_file_and_get_grammar("g8.txt")
	print(g8.derives_epsilon('B'))


	'''leftSides = ['S', 'A', 'B', 'C', 'D']
	rightSides = ['0 S', 'id A B', '0', '0B', '1S', '1', '0 A', '1 B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
					Production(leftSides[0], 'A B'),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]), Production(leftSides[1], '&'),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7]), Production('B', 'C D'),
				   Production(leftSides[3], '&'),Production(leftSides[4], 'x')]'''
	#print(Globals.grammar_count)
	#myGrammar = Grammar(productions)
	#print(myGrammar)
	#print(myGrammar.derives_epsilon('S', ''))

	'''
		S -> AB | CD
		A -> aB | a
		B -> bB | b

		C -> XY
		D -> dD | &

		X -> xX | &
		Y -> yY |&
	'''


	'''productions = [
		Production('S', 'A B'), Production('S', 'C D'),
		Production('A', 'a A'), Production('A', 'a'),
		Production('B', 'b B'), Production('B', 'b'),
		Production('C', 'X Y'),
		Production('D', 'd D'), Production('D', '&'),
		Production('X', 'x X'), Production('X', '&'),
		Production('Y', 'y Y'), Production('Y', '&'),
	]

	g = Grammar(productions)
	print(g)
	print(g.derives_epsilon('S'))'''
