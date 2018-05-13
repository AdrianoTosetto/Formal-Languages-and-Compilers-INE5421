from deterministic_automaton import *
from globals import *

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
			return self.currentStates
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
