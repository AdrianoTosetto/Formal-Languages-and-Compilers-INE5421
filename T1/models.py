class Automaton:

	def __init__(self, states, finalStates, initialState, Σ=['0','1']):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentState = initialState
		self.Σ = Σ

	def process_input(self, input):
		for symbol in input:
			print(self.currentState)
			self.currentState = self.currentState.next_state(symbol)
	def next_state(self, symbol):
		self.currentState = self.currentState.next_state(symbol)
		return self.currentState


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
	def __init__(self, name):
		self.name = name
		self.ndtransitions = []

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
class NDAutomaton:
	def __init__(self, states, finalStates, initialState):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentStates = [initialState]

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
			return self.currentStates
		else:
			return temp

	def transition_table(self):
		already_visited = []
		Σ = ['0','1']


class State:
	def __init__(self, name):
		self.name = name
		self.transitions = []

	def __str__(self):

		return self.name

	def __repr__(self):
		return self.__str__()

	def next_state(self, symbol):
		for t in self.transitions:
			print(t)
			if t.get_symbol() == symbol:
				return t.get_next_state()
		return None

	def __eq__(self, other):
		return self.name == other

	def add_transition(self, t):
		self.transitions.append(t)

#-------------------------------------------------------------------------------

class Grammar:
	def __init__(self, productions):
		self.productions = productions

	def produce(self, size):
		sentences = []
		sForms = [self.productions[0].leftSide]
		while len(sForms) != 0:
			curr_sym = sForms[0][-1]
			for prods in self.productions:
				if curr_sym == prods.leftSide[-1]:
					#curr_form = (sForms[0] - sForms[0][-1]) + prods.rightSide
					curr_form = "".join(sForms[0].rsplit(sForms[0][-1]))
					curr_form = curr_form + prods.rightSide
					if len(curr_form) <= size:
						#print("Passou")
						if all(s.isdigit() or s.islower() for s in curr_form):
							print(curr_form)
							sentences.append(curr_form)
						else:
							sForms.append(curr_form)
			#"".join(sForms[0].rsplit(sForms[0][-1]))
			sForms.pop(0)
		return sentences
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
			leftSides.add(prods.leftSide)
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
		initialState = states['S']
		finalStates = [λ]
		if self.has_empty_sentence():
			finalStates.append(initialState)
		
		return NDAutomaton(states.values(), finalStates, initialState)

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

'''class SententialForm:
	def __init__(self, symbols):
		self.symbols = symbols
	def __str__(self):
		return self.symbols
	def __add__(self, form):
		return SententialForm(self.symbols + form.symbols)
	def __sub__(self, index):
		return SententialForm("".join(self.symbols.rsplit(self.symbols[index])))'''

if __name__ == "__main__":

	leftSides = ['S', 'A', 'B']
	rightSides = ['0S', '1A', '0', '0B', '1S', '1', '0A', '1B']
	productions = [Production(leftSides[0], rightSides[0]), Production(leftSides[0], rightSides[1]), Production(leftSides[0], rightSides[2]),
				   Production(leftSides[1], rightSides[3]), Production(leftSides[1], rightSides[4]), Production(leftSides[1], rightSides[5]),
				   Production(leftSides[2], rightSides[6]), Production(leftSides[2], rightSides[7])]
	myGrammar = Grammar(productions)
	#print(myGrammar)
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

	#print(myGrammar)
	#myGrammar.convert_to_automaton()