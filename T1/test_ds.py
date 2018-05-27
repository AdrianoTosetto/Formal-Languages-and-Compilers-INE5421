from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *

if __name__ == "__main__":
	expr = '( 1 | 0 ) ? . ( ( 1 . 0 ) * . ( 0 . 1 ) ) * . ( 1 | 0 ) ?'
	t = Tree()
	nodo = t.build(polish_notation(expr))
	t.costura()
	test = nodo.left.right.left.right.right
	print("test = " + str(test))
	print(test.handle_leaf())
	#display(nodo,1)