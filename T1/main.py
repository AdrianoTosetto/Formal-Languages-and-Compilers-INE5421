from structures import *
from regular_grammar import *
from non_deterministic_automaton import *
from deterministic_automaton import *
from globals import *
from operations_with_automata import *
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
	Globals.grammars.append(myGrammar)

	leftSides1 = ['S', 'A', 'B', 'C']
	rightSides1 = ['aA', 'bB', 'aS', 'bC', 'b', 'bS', 'aC', 'a', 'aB', 'bA']
	productions1 = [Production(leftSides1[0], rightSides1[0]), Production(leftSides1[0], rightSides1[1]),
	 				Production(leftSides1[1], rightSides1[2]), Production(leftSides1[1], rightSides1[3]), Production(leftSides1[1], rightSides1[4]),
				   	Production(leftSides1[2], rightSides1[5]), Production(leftSides1[2], rightSides1[6]), Production(leftSides1[2], rightSides1[7]),
				   	Production(leftSides1[3], rightSides1[8]), Production(leftSides1[3], rightSides1[9])]
	#print(Globals.grammar_count)
	myGrammar1 = Grammar(productions1)
	Globals.grammars.append(myGrammar1)
	#m = MainWindow()

	#print(myGrammar1)
	'''a = myGrammar1.convert_to_automaton()
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
	#display(n19,1)
	t = Tree()
	s = polish_notation("( C . B | A ? ) *")
	r = t.build(s)
	r.costura()'''

	#t.costura()
	#display(t.root,1)

	#print(n19.enumerate())
	#print(n19.most_left_node())

	#-polish_notation("( A . B | A . C ) * . A ? | ( B A ? C ) *")
	#print("traversal = " + str(traversal))

	#display(n19, 1)
	'''q0 = State('q0', True)
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

	print(a1)'''

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
	q11 = State('q11', True)

	t1  = Transition('a',q2)
	t2  = Transition('b',q3)
	#t3  = Transition('c',q6)
	t3  = Transition('c',q11)

	q1.add_transition(t1)
	q1.add_transition(t2)
	q1.add_transition(t3)

	t4  = Transition('a',q1)
	t5  = Transition('b',q7)
	t6  = Transition('c',q10)

	q2.add_transition(t4)
	q2.add_transition(t5)
	q2.add_transition(t6)

	t7  = Transition('b',q5)
	t8  = Transition('c',q4)

	q3.add_transition(t7)
	q3.add_transition(t8)

	t9  = Transition('b',q3)
	q4.add_transition(t9)

	t10 = Transition('b',q3)
	t11 = Transition('c',q6)
	q5.add_transition(t10)
	q5.add_transition(t11)


	t12 = Transition('b',q5)
	q6.add_transition(t12)


	t13 = Transition('b',q8)
	t14 = Transition('c',q9)

	q7.add_transition(t13)
	q7.add_transition(t14)

	t15 = Transition('b',q7)
	t16 = Transition('c',q10)

	q8.add_transition(t15)
	q8.add_transition(t16)

	t17 = Transition('b',q7)
	q9.add_transition(t17)

	t18 = Transition('b',q8)
	q10.add_transition(t18)

	t19 = Transition('b',q5)
	q11.add_transition(t19)'''

	'''
	q0 = State('q0', True)
	q1 = State('q1')
	q2 = State('q2')
	q3 = State('q3')
	q4 = State('q4', True)
	q5 = State('q5')
	q6 = State('q6', True)

	t1 = Transition('a', q1)
	t2 = Transition('b', q2)
	t3 = Transition('c', q3)
	q0.add_transition(t1)
	q0.add_transition(t2)
	q0.add_transition(t3)

	#t4 = Transition('a', q1)
	t5 = Transition('b', q4)
	t6 = Transition('c', q5)
	#q1.add_transition(t4)
	q1.add_transition(t5)
	q1.add_transition(t6)

	t7 = Transition('a', q6)
	t8 = Transition('b', q4)
	t9 = Transition('c', q5)
	q2.add_transition(t7)
	q2.add_transition(t8)
	q2.add_transition(t9)

	t10 = Transition('a', q6)
	t11 = Transition('b', q4)
	#t12 = Transition('c', q2)
	q3.add_transition(t10)
	q3.add_transition(t11)
	#q3.add_transition(t12)


	t13 = Transition('a', q1)
	t14 = Transition('b', q2)
	t15 = Transition('c', q3)
	q4.add_transition(t13)
	q4.add_transition(t14)
	q4.add_transition(t15)

	t16 = Transition('a', q1)
	t17 = Transition('b', q2)
	#t18 = Transition('c', q2)
	q5.add_transition(t16)
	q5.add_transition(t17)
	#q5.add_transition(t19)

	#t19 = Transition('a', q1)
	t20 = Transition('b', q2)
	t21 = Transition('c', q3)
	#q6.add_transition(t19)
	q6.add_transition(t20)
	q6.add_transition(t21)

	a = Automaton([q0,q1,q2,q3,q4,q5,q6], [q0,q4,q6], q0, ['a','b','c'])
	print(a)
	print(a.minimize())
	'''

	'''
	expr = 'A | ( B . B )'
	t = BinaryTree()
	nodo = t.build(polish_notation(expr))
	#print(nodo.right.symbol)
	display(nodo,1)
	'''

	'''q0_1 = State('q0', True)
	q1_1 = State('q1', True)

	t1 = Transition('a', q0_1)
	t2 = Transition('b', q1_1)
	t3 = Transition('a', q0_1)

	q0_1.add_transition(t1)
	q0_1.add_transition(t2)
	q1_1.add_transition(t3)

	a1 = Automaton([q0_1, q1_1], [q0_1, q1_1], q0_1, ['a', 'b'])

	q0_2 = State('q0', True)
	q1_2 = State('q1', True)

	t4 = Transition('b', q0_2)
	t5 = Transition('a', q1_2)
	t6 = Transition('b', q0_2)

	q0_2.add_transition(t4)
	q0_2.add_transition(t5)
	q1_2.add_transition(t6)

	a2 = Automaton([q0_2, q1_2], [q0_2, q1_2], q0_2, ['a', 'b'])

	a3 = automata_union(a1, a2)
	a3 = a3.determinize()
	for s in a3.states:
		print("state " + str(s) + " isAcceptance? " + str(s.isAcceptance))
	print(a3.minimize())'''


	'''q0 = State('q0', True)
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
	a1 = automata_complement(a)
	#a1 = make_nondeterministic(a)
	print(a)
	print(a1)'''

	'''expr = '( D . C * ) . ( A . B )'
	t = Tree()
	nodo = t.build(polish_notation(expr))
	t.costura()
	test = nodo.most_left_node()
	print(test.handle_leaf())
	#print(nodo.right.symbol)
	display(nodo,1)'''

	'''q0 = State('q0')
	qr0 = State('qr0', True)
	qr1 = State('qr1')
	qr2 = State('qr2')

	t1 = Transition('0', qr0)
	t2 = Transition('1', qr1)
	q0.add_transition(t1)
	q0.add_transition(t2)

	t3 = Transition('0', qr0)
	t4 = Transition('1', qr1)

	qr0.add_transition(t3)
	qr0.add_transition(t4)

	t5 = Transition('0', qr2)
	t6 = Transition('1', qr0)

	qr1.add_transition(t5)
	qr1.add_transition(t6)

	t7 = Transition('0', qr1)
	t8 = Transition('1', qr2)

	qr2.add_transition(t7)
	qr2.add_transition(t8)

	div3 = Automaton(set([q0, qr0, qr1, qr2]),set([qr0]), q0, ['0','1'])


	_q0 = State('_q0')
	_qr0 = State('_qr0', True)
	_qr1 = State('_qr1')

	_t1 = Transition('0', _qr0)
	_t2 = Transition('1', _qr1)
	_q0.add_transition(_t1)
	_q0.add_transition(_t2)

	_t3 = Transition('0', _qr0)
	_t4 = Transition('1', _qr1)

	_qr0.add_transition(_t3)
	_qr0.add_transition(_t4)

	_t5 = Transition('0', _qr0)
	_t6 = Transition('1', _qr1)

	_qr1.add_transition(_t5)
	_qr1.add_transition(_t6)

	div2 = Automaton(set([_q0, _qr0, _qr1]),set([_qr0]), _q0, ['0','1'])

	print(div2)
	print(div3)'''

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

	nbs = Automaton(set([q0_0,q1_0]),set([q0_0,q1_0]),q0_0,['a','b'])
	nas = Automaton(set([q0_1,q1_1]),set([q0_1,q1_1]),q0_1,['a','b'])

	print(automata_difference(nbs, nas))

	print(areEqual(nbs, getReverse(nas)))


	expr = '( 1 | 0 ) ? . ( ( 1 . 0 ) * . ( 0 . 1 ) ) * . ( 1 | 0 ) ?'
	t = Tree()
	nodo = t.build(polish_notation(expr))
	t.costura()
	test = nodo.most_left_node().costura_node.right
	#print("test = " + str(test))
	#print(test.handle_leaf())
	#print(nodo.right.symbol)
	#display(nodo,1)
