'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

from context_free_grammar import *

if __name__ == "__main__":

	leftSides = ['S', 'A', 'B']
	rightSides = ['0S', '111A B', '0', '0B', '1S', '1', '0A', '1B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	#print(Globals.grammar_count)
	myGrammar = Grammar(productions)
	print(myGrammar)

