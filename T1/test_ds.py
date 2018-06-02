from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *

if __name__ == "__main__":
	#expr = '( 1 | 0 ) ? . ( ( 1 . 0 ) * . ( 0 . 1 ) ) * . ( 1 | 0 ) ?'
	#expr = ' ( ( C . D * ) * ) ? . B'
	#expr = '( ( C * | ( A . D ) ? ) . ( A . B ) * ) ?'
	#expr = '( A * ) *'
	expr = '( A . B . C ) * | ( C . B . A ) *'
	re = RegExp(expr)
	re.to_automaton()