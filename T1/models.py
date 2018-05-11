class Automaton:

	def __init__(self, states, finalStates, initialState, Σ=['0','1']):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentState = initialState
		self.Σ = Σ
		self.equi_classes = []

	def process_input(self, input):
		for symbol in input:
			print(self.currentState)
			self.currentState = self.currentState.next_state(symbol)
			if self.currentState is None:
				return False

		return self.currentState.isAcceptance

	def next_state(self, symbol):
		self.currentState = self.currentState.next_state(symbol)
		return self.currentState

	def __str__(self):
		stringerson = "   δ"
		Σ = sorted(self.Σ)
		for σ in Σ:
			stringerson = stringerson + " | " + σ
		stringerson = stringerson + "\n"
		for s in self.states:
			if s.name == self.initialState.name:
				stringerson = stringerson + "->"
			else:
				stringerson = stringerson + "  "
			if s in self.finalStates:
				stringerson = stringerson + "*"
			else:
				stringerson = stringerson + " "
			stringerson = stringerson + s.__str__()
			for σ in Σ:
				if σ in s.get_symbols():
					stringerson = stringerson + " | " + s.next_state(σ).__str__()
				else:
					stringerson = stringerson + " | -"
			stringerson	= stringerson + "\n"
		return stringerson

	def __repr__(self):
		return str(self)
	def get_acceptance_states(self):
		ret = []
		for s in self.states:
			if s.isAcceptance:
				ret.append(s)
		return ret
	def get_non_acceptance_states(self):
		ret= []
		for s in self.states:
			if not(s.isAcceptance):
				ret.append(s)
		return ret
	def belong_same_equi_class(self, q0, q1):
		for eqclass in self.equi_classes:
			if q0 in eqclass and q1 in eqclass:
				return True
		return False
	def remove_unreacheable_states(self):
		test_states = set(self.states) - {self.initialState}

		for s in test_states.copy():
			if not self.has_path(self.initialState, s):
				self.states.remove(s)
				self.remove_transitions_from(s)
	def remove_transitions_from(self, st):
		for state in self.states:
			for t in state.transitions:
				if t.target_state == st:
					t.target_state = φ(self.Σ)


	def remove_dead_states(self):
		for s in set(self.states) - set(self.finalStates):
			for fs in self.finalStates:
				if not self.has_path(s, fs):
					try:
						self.states.remove(s)
						self.remove_transitions_from(s)
						continue
					except ValueError:
						pass

	def has_path(self, q0, q1):
		'''if q0 == q1:
			return True
		visited = set([q0])
		to_visit = visited
		temp = to_visit
		while(len(to_visit) != 0):
			for symbol in self.Σ:
				for s in to_visit.copy():
					temp = to_visit - {s}
					ns = s.next_state(symbol)
					if ns is None:
						continue
					if ns not in visited:
						temp.add(ns)
					visited.add(ns)
				to_visit = temp
				temp = set()
		return q1 in visited'''

		return q1 in self.depth_first_search(q0)
	def next_states_all(self, s):
		ret = []
		for symbol in self.Σ:
			if s.next_state(symbol) is not None:
				ret.append(s.next_state(symbol))

		return ret

	def depth_first_search(self, s):

		visited = set()
		stack = [s]

		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.add(vertex)
				stack.extend((self.next_states_all(vertex)))

		return visited
	def minimize(self):
		self.remove_dead_states()
		self.remove_unreacheable_states()
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]
		temp = self.equi_classes
		print(self.equi_classes)
		'''for eqclass in self.equi_classes:
			for state in eqclass:
				test_states = eqclass - {state}
				for ts in test_states:
					for symbol in self.Σ:
						n1 = state.next_state(symbol)
						n2 = ts.next_state(symbol)
						if not self.belong_same_equi_class(n1, n2):
							#print(str(n1) + ' ' + str(n2) + ' nao pertencem')
							self.equi_classes.remove(eqclass)
							eqclass = eqclass - {ts}
							self.equi_classes.append({ts})
							self.equi_classes.append(eqclass)'''
	def complete(self):
		for s in self.states:
			s.complete(self.Σ)
class Transition:
	def __init__(self, symbol, target_state):
		self.target_state = target_state
		self.symbol = symbol
	def get_symbol(self):
		return self.symbol
	def get_next_state(self):
		return self.target_state
	def __str__(self):
		return self.symbol + " -> " + self.target_state.__str__()

class State:

	def __init__(self, name, isAcceptance = False):
		self.name = name
		self.transitions = []
		self.isAcceptance = isAcceptance

	def get_symbols(self):
		symb = set()
		for t in self.transitions:
			symb.add(t.symbol)
		return symb

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def next_state(self, symbol):
		for t in self.transitions:
			#print(t)
			if t.get_symbol() == symbol:
				return t.get_next_state()
		return None

	def add_transition(self, t):
		self.transitions.append(t)

	def __hash__(self):
		hashable = self.name
		if self.name == 'λ':
			hashable ='lambda'
		return sum([ord(c) for c in hashable])

	def __eq__(self, other):
		return self.name == other.name
	def complete(self, Σ):
		add_t = True
		for symbol in Σ:
			for t in self.transitions:
				if t.symbol == symbol:
					add_t = False
					continue
				else:
					add_t = True
			if add_t:
				nt = Transition(symbol, φ(Σ))
				self.transitions.append(nt)
				add_t = False

'''
	error state
'''

class φ(State):
	def __init__(self, Σ):
		State.__init__(self, "phi")
		for symbol in Σ:
			t = Transition(symbol, self)
			self.transitions.append(t)
	def next_state(self, symbol):
		return self
	def __str__(self):
		return "φ"


#-------------------------------------------------------------------------------

class NDTransition:
	def __init__(self, symbol, target_states):
		self.target_states = target_states
		self.symbol = symbol
	def get_symbol(self):
		return self.symbol
	def get_next_states(self):
		return self.target_states

	def __str__(self):
		ret = self.symbol + " -> ["
		ret = ret + ",".join(s.__str__() for s in self.target_states)
		ret = ret + "]"
		return ret
	def __repr__(self):
		return self.__str__()

class NDState:
	def __init__(self, name, isAcceptance = False):
		self.name = name
		self.ndtransitions = []
		self.isAcceptance = isAcceptance

	def get_symbols(self):
		symb = set()
		for t in self.ndtransitions:
			symb.add(t.symbol)
		return symb

	def __str__(self):
		return self.name
	def __repr__(self):
		return self.__str__()
	def next_states(self, symbol):
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				return t.get_next_states()
		return None
	def next_states_str(self, symbol):
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				return t.__str__()
		return None
	def add_transition(self, t):
		self.ndtransitions.append(t)
		self.complete()

	def __hash__(self):
		return id(self)

	def __eq__(self, other):
		return self.name == other.name


class NDAutomaton:
	def __init__(self, states, finalStates, initialState, Σ=['0','1']):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentStates = [initialState]
		self.Σ = Σ

	def process_input(self, input):
		return None
		#for symbol in input:
		#	print(self.currentState)
		#	self.currentState = self.currentState.next_state(symbol)
	def next_states(self, symbol, go_ahead=True):
		temp = []
		for state in self.currentStates:
			s = state.next_states(symbol)
			if s is not None:
				temp.extend(s)
		#remove duplicated states
		temp = list(set(temp))
		if go_ahead:
			self.currentStates = temp
			return self.curaddrentStates
		else:
			return temp

	def transition_table(self):
		already_visited = []
		Σ = ['0','1']

	def __str__(self):
		stringerson = "   δ"
		Σ = sorted(self.Σ)
		for σ in Σ:
			stringerson = stringerson + " |  " + σ + " "
		stringerson = stringerson + "\n"
		for s in self.states:
			if s == self.initialState:
				stringerson = stringerson + "->"
			else:
				stringerson = stringerson + "  "
			if s in self.finalStates:
				stringerson = stringerson + "*"
			else:
				stringerson = stringerson + " "
			stringerson = stringerson + s.__str__()
			for σ in Σ:
				if σ in s.get_symbols():
					stringerson = stringerson + " | " + s.next_states(σ).__str__()
				else:
					stringerson = stringerson + " |  - "
			stringerson	= stringerson + "\n"
		return stringerson

	def __repr__(self):
		return str(self)

	'''
		determinization functions:
	'''

	def determinize_states(self, states, finalStates, newStates):
		if len(states) == 1:
			newState = State(list(states)[0].name)
			newStates.add(newState)
			if list(states)[0] in self.finalStates:
				finalStates.add(newState)
			return newState
		newState = State(states.__str__())
		for a in self.Σ:
			nextStates = set()
			for s in states:
				for t in s.ndtransitions:
					if t.symbol == a:
						nextStates = nextStates | set(t.target_states)
			newState.add_transition(Transition(a, self.determinize_states(nextStates, finalStates, nextStates)))
		if any(s in self.finalStates for s in states):
			finalStates.add(newState)
		if newState in newStates:
			newStates.remove(newState)
		newStates.add(newState)
		return newState

	def determinize(self):
		newStates = set()
		finalStates = set()
		for s in self.states:
			newState = State(s.name)
			newStates.add(newState)
		for s in self.finalStates:
			newFinalState = State(s.name)
			finalStates.add(newFinalState)
		for s in self.states:
			newState = State(s.name)
			for t in s.ndtransitions:
				newState.add_transition(Transition(t.symbol, self.determinize_states(t.target_states, finalStates, newStates)))
			if newState in newStates:
				newStates.remove(newState)
			newStates.add(newState)
		print(newStates)
		print(finalStates)
		return Automaton(newStates, finalStates, self.initialState, self.Σ)





#-------------------------------------------------------------------------------

'''
	for regular grammars only
'''

class Grammar:
	def __init__(self, productions):
		self.productions = productions

	'''
		this function outputs all the sentences generated by this grammar with
		size less than or equal to the argument "size"
	'''
	def produce(self, size):
		sentences = []
		sForms = [self.productions[0].leftSide]
		while len(sForms) != 0:
			curr_sym = sForms[0][-1]
			for prods in self.productions:
				if curr_sym == prods.leftSide[-1]:
					curr_form = "".join(sForms[0].rsplit(sForms[0][-1]))
					curr_form = curr_form + prods.rightSide
					if len(curr_form) <= size:
						#print("Passou")
						if all(s.isdigit() or s.islower() or s == '&' for s in curr_form):
							print(curr_form)
							if ('&' in curr_form and len(curr_form) > 1):
								curr_form = "".join(sForms[0].rsplit('&'))
							sentences.append(curr_form)
						else:
							sForms.append(curr_form)
			sForms.pop(0)
		return sentences

	def getAlphabet(self):
		Σ = set()
		for prod in self.productions:
			Σ.add(prod.rightSide[0])
		return list(Σ)

	def has_empty_sentence(self):
		for p in self.productions:
			if p.leftSide == 'S' and p.rightSide == '&':
				return True
		return False

	def __str__(self):
		stringerson = ""
		leftSides = set()
		first = True
		for prods in self.productions:
			if prods.leftSide != self.productions[0].leftSide:
				leftSides.add(prods.leftSide)
		leftSides = [self.productions[0].leftSide] + sorted(leftSides)
		for lefts in leftSides:
			for prods in self.productions:
				if first and lefts is prods.leftSide:
					stringerson = stringerson + lefts + " -> " + prods.rightSide
					first = False
				elif lefts is prods.leftSide:
					stringerson = stringerson + " | " + prods.rightSide
			stringerson = stringerson + "\n"
			first = True
		return stringerson

	def get_non_terminals(self):
		ret = []
		for p in self.productions:
			ret.append(p.leftSide)

		return list(set(ret))

	'''
		this function outputs the productions of a given non-terminal
		e.g if the non_terminal has the following productions:  B -> bS | aC | a,
		the function is supposed to output [bS, aC, a]
	'''
	def get_productions_from(self, non_terminal):
		ret = []
		for p in self.productions:
			if p.leftSide == non_terminal:
				ret.append(p.rightSide)
		return ret

	'''
		this functions outputs the productions in lexical order
		e.g: if the non_terminal has the following productions: B -> bS | aC | a,
		the functions is supposed to output [a, aC, bS]
	'''
	def get_ord_productions_from(self, non_terminal):
		ret = []
		for p in self.productions:
			if p.leftSide == non_terminal:
				ret.append(p.rightSide)
		return sorted(ret, key=str.lower)

	'''
		this functions works the same way as the function above, but it outputs
		the productions in lists. E.g: if the non_terminal has the following productions: B -> bS | aC | a,
		the functions is supposed to output [[a, aC], [bS]]
	'''
	def _get_ord_productions_from(self, non_terminal):
		sorted = self.get_ord_productions_from(non_terminal)
		lastSymbol = sorted[0][0]
		add = []
		ret = []
		t = 0
		for p in sorted:
			if p[0] == lastSymbol:
				add.append(p)
			else:
				ret.append(add)
				lastSymbol = p[0]
				add = []
				add.append(p)
		ret.append(add)
		return ret

	def convert_to_automaton(self):
		alphabet = self.getAlphabet()
		states = {s:NDState(s) for s in self.get_non_terminals()}
		# state that accepts the input
		λ = NDState('λ')
		for s in states:
			prods = self._get_ord_productions_from(s.__str__())
			for prod in prods:
				sset = []
				for i in prod:
					symbol = i[0] #terminal symbol
					if len(i) == 1:
						sset.append(λ)
					else:
						nt = i[1]
						next_state = states[nt]
						sset.append(next_state)
				t = NDTransition(symbol, sset)
				#print(states[s].__str__() + " goes to " + str(sset) + " for " + symbol)
				sset = []
				states[s].add_transition(t)

		states['λ'] = λ

		initialState = states['S']
		finalStates = [λ]
		if self.has_empty_sentence():
			finalStates.append(initialState)

		return NDAutomaton(states.values(), finalStates, initialState, alphabet)

class Production:
	def __init__(self, leftSide, rightSide):
		self.leftSide = leftSide
		self.rightSide = rightSide

	def __str__(self):
		return self.leftSide + " -> " + self.rightSide

	def __repr__(self):
		return str(self)

	def isTerminalProduction(self):
		return len(self.rightSide) == 1

#-------------------------------------------------------------------------------

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

	print(myGrammar1)
	a = myGrammar1.convert_to_automaton()
	print(a.next_states('a')) #should output [A] and it does!
	print(a.next_states('b')) #should output [C, λ] and it does!
	print("")
	print(myGrammar)
	b = myGrammar.convert_to_automaton()
	print(b.next_states('0'))
	print(b.next_states('1'))
	print(a)
	print(b)
	a1 = a.determinize()
	print(a1)'''

	q0 = State('q0')
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
	#q5.add_transition(t12)
	#q5.complete(['a','b'])
	#print(q5.transitions[1])
	states = [q0,q1,q2,q3,q4,q5]
	finalStates = [q4,q5]
	initialState = q0


	a = Automaton(states,finalStates, initialState, ['a','b'])
	print(a)
	a.complete()
	print(a)
	a.remove_dead_states()
	print(a)
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
	#print(a.process_input('b'))
