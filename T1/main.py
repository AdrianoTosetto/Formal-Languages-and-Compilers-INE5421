from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *

if __name__ == "__main__":

	'''leftSides = ['S', 'A', 'B']
	rightSides = ['0S', '1A', '0', '0B', '1S', '1', '0A', '1B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	myGrammar = Grammar(productions)

	leftSides1 = ['S', 'A', 'B', 'C']
	rightSides1 = ['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
	productions1 = [Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
	 				Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
				   	Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
				   	Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]
	myGrammar1 = Grammar(productions1)

	#print(myGrammar1)
	a = myGrammar1.convert_to_automaton()
	print(a.next_states('a')) #should output [A] and it does!
	print(a.next_states('b')) #should output [C, λ] and it does!
	print("")
	print(myGrammar)
	b = myGrammar.convert_to_automaton()
	#print(a)
	#print(b)
	a1 = a.determinize()
	#print(a1)
	print(myGrammar1)'''

	'''q0 = State('q0')
	q1 = State('q1')
	q2 = State('q2')
	q3 = State('q3')
	q4 = State('q4', True)
	q5 = State('q5', True)

	t1 = Transition('a', q1)
	t2 = Transition('b', q2)

	q0.add_transition(t1)
	#q0.add_transition(t2)

	t3 = Transition('a', q4)
	t4 = Transition('b', q4)

	q1.add_transition(t3)
	q1.add_transition(t4)

	t5 = Transition('a', q2)
	t6 = Transition('b', q2)

	q2.add_transition(t5)
	q2.add_transition(t6)

	t7 = Transition('a', q4)
	t8 = Transition('b', q4)

	q3.add_transition(t7)
	q3.add_transition(t8)

	t9  = Transition('a', q5)
	t10 = Transition('b', q5)

	q4.add_transition(t9)
	q4.add_transition(t10)

	t11 = Transition('a', q4)
	t12 = Transition('b', q4)

	q5.add_transition(t11)
	q5.add_transition(t12)
	#q5.complete(['a','b'])
	#print(q5.transitions[1])
	states = [q0,q1,q2,q3,q4,q5]
	finalStates = [q4,q5]
	initialState = q0


	a = Automaton(states,finalStates, initialState, ['a','b'])
	a.minimize()
	#print(a.states[5].transitions[1])
	#a.remove_unreacheable_states()
	#a.remove_dead_states()
	#print(a)

	#a.remove_unreacheable_states()
	#a.remove_dead_states()
	#print(a)
	#print(a.breadth_first_search(q0))
	#print(a.has_path(q0, q2))
	#print(a.belong_same_equi_class(q3,q1))
	#print(a.process_input('b'))'''

	'''q1 = State('q1')
	q2 = State('q2', True)
	q3 = State('q3', True)
	q4 = State('q4')
	q5 = State('q5')
	q6 = State('q6', True)
	q7 = State('q7')
	q8 = State('q8', True)
	q9 = State('q9', True)
	q10 = State('q10')

	t1 = Transition('a', q2)
	t2 = Transition('a', q1)

	t3 = Transition('b', q3)
	t4 = Transition('b', q4)
	t5 = Transition('b', q9)
	t3a = Transition('b', q3)
	t4a = Transition('b', q4)

	t6 = Transition('c', q6)
	t7 = Transition('c', q5)
	t8 = Transition('c', q7)
	t9 = Transition('c', q8)
	t10 = Transition('c', q10)
	t7a = Transition('c', q5)
	t6a = Transition('c', q6)

	q1.add_transition(t1)
	q1.add_transition(t3)
	q1.add_transition(t6)

	q2.add_transition(t2)
	q2.add_transition(t4)
	q2.add_transition(t7)

	q3.add_transition(t8)

	q4.add_transition(t9)

	q5.add_transition(t5)

	q6.add_transition(t10)

	q7.add_transition(t3a)

	q8.add_transition(t4a)

	q9.add_transition(t7a)

	q10.add_transition(t6a)

	states = [q1, q2, q3, q4, q5, q6, q7, q8, q9,q10]
	finalStates = [q2, q3, q6, q8, q9]
	a = Automaton(states,finalStates, q1, ['a','b','c'])
	print(a)
	#print(a.equi_classes)
	a.minimize()
	print(a)'''
	'''n1 = Node('a')
	n2 = Node('b')
	n3 = Node('.', n1, n2)

	n4 = Node('a')
	n5 = Node('c')
	n6 = Node('.', n4, n5)
	n7 = Node('|', n3, n6)
	n8 = Node('*', n7)
	n9 = Node('a')
	n10 = Node('?', n9)
	n11 = Node('.', n8, n10)

	n12 = Node('a')
	n13 = Node('?', n12)
	n14 = Node('b')
	n15 = Node('.', n14, n13)
	n16 = Node('c')
	n17 = Node('.', n15, n16)
	n18 = Node('*', n17)

	n19 = Node('|',n11,n18)

	n19.post_order()
	print(n19.traversal)

	polish_notation("( A . B | A . C ) * . A ? | ( B A ? C ) *")
	print(traversal)

	display(n19, 1)'''
	q0 = State('q0', True)
	q1 = State('q1')
	q2 = State('q2', True)

	t1 = Transition('a', q1)
	t2 = Transition('b', q2)
	q0.add_transition(t1)
	q0.add_transition(t2)

	t3 = Transition('a', q0)
	t4 = Transition('b', q1)
	q1.add_transition(t3)
	q1.add_transition(t4)

	t5 = Transition('a', q1)
	t6 = Transition('b', q2)
	q2.add_transition(t5)
	q2.add_transition(t6)

	a = Automaton([q0,q1,q2],[q0,q2], q0,['a','b'])
	print(a)
	a1 = a.minimize()
	print(a.process_input("aaabaa"))

	print(a1)
	#print(a.process_input('aaaa'))