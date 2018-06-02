from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *
from operations_with_grammars import *
import sys
sys.path.append('view/')
from main_window import *

if __name__ == "__main__":

	leftSides = ['S', 'A', 'B']
	rightSides = ['0S', '1A', '0', '0B', '1S', '1', '0A', '1B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	#print(Globals.grammar_count)
	myGrammar = Grammar(productions)
	#Globals.grammars.append(myGrammar)

	leftSides1 = ['S', 'A', 'B', 'C']
	rightSides1 = ['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
	productions1 = [Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
	 				Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
				   	Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
				   	Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]
	#print(Globals.grammar_count)
	myGrammar1 = Grammar(productions1)
	#Globals.grammars.append(myGrammar1)
	print(grammar_kleene_star(myGrammar))
	print(myGrammar)
	for p in grammar_kleene_star(myGrammar).produce(5):
		print(p)

	q0_0 = State('q0_0', True)
	q1_0 = State('q1_0', True)

	t0_0 = Transition('a', q0_0)
	t1_0 = Transition('b', q1_0)
	t2_0 = Transition('a', q0_0)

	q0_0.add_transition(t0_0)
	q0_0.add_transition(t1_0)
	q1_0.add_transition(t2_0)

	q0_1 = State('q0_1', True)
	q1_1 = State('q1_1', True)

	t0_1 = Transition('b', q0_1)
	t1_1 = Transition('a', q1_1)
	t2_1 = Transition('b', q0_1)

	q0_1.add_transition(t0_1)
	q0_1.add_transition(t1_1)
	q1_1.add_transition(t2_1)

	nbs = Automaton(set([q0_0,q1_0]),set([q0_0,q1_0]),q0_0,['a','b'], add = True)
	nas = Automaton(set([q0_1,q1_1]),set([q0_1,q1_1]),q0_1,['a','b'], add = True)

	print(automata_difference(nbs, nas, add = True))

	print(areEqual(nbs, getReverse(nas)))


	expr = '( 1 | 0 ) ? . ( ( 1 . 0 ) * . ( 0 . 1 ) ) * . ( 1 | 0 ) ?'
	t = Tree()
	nodo = t.build(polish_notation(expr))
	t.costura()
	test = nodo.most_left_node().costura_node.right
	win = MainWindow()
	#print("test = " + str(test))
	#print(test.handle_leaf())
	#print(nodo.right.symbol)
	#display(nodo,1)
