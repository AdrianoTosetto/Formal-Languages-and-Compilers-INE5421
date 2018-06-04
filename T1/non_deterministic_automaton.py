from deterministic_automaton import *
from globals import *
import copy

class NDTransition:
	def __init__(self, symbol, target_states):
		self.target_states = target_states
		self.symbol = symbol
	def get_symbol(self):
		return self.symbol
	def get_next_states(self):
		return self.target_states

	def setOriginState(self, state):
		self.originState = state

	def __str__(self):
		ret = "δ(" + str(self.originState) + "," + str(self.symbol) + ") = ["
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

	def next_states(self, symbol, already_visited=set()):

		next_states = set()
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				next_states = set(t.get_next_states()) - already_visited
				already_visited = already_visited | next_states
				for s in next_states:
					already_visited = already_visited | s.next_states('&', already_visited)

		return already_visited
	def next_states_no_epsilon(self, symbol):
		next_states = set()
		if symbol == "&":
			return
	def next_states_str(self, symbol):
		for t in self.ndtransitions:
			if t.get_symbol() == symbol:
				return t.__str__()
		return None
	def add_transition(self, t):
		if self.ndtransitions == None:
			self.ndtransitions = [t]
		else:
			self.ndtransitions.append(t)
		t.setOriginState(self)

	def __hash__(self):
		hashable = self.name
		if self.name == 'λ':
			hashable ='lambda'
		elif self.name == 'φ':
			hashable = 'phi'
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def has_epsilon_transition(self):
		for t in self.ndtransitions:
			if t.symbol == '&':
				return True
		return False


class NDAutomaton:
	def __init__(self, states, finalStates, initialState, Σ=['0','1'], name = None, add = False):
		if len(states) < 1:
			return None
		if name is None:
			self.name = 'M' + str(Globals.automaton_count)
			Globals.automaton_count += 1
		else:
			self.name = name
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentStates = {initialState} | initialState.next_states('&')
		self.Σ = Σ
		if self not in Globals.automata and add:
			Globals.automata.append(self)

	def process_input(self, input):
		for symbol in input:
			ns = set()
			for cs in self.currentStates:
				ns = ns | cs.next_states(symbol)
			self.currentStates = ns
			#print(self.currentStates)
			if self.currentStates is set():
				self.currentStates = {self.initialState} | self.initialState.next_states('&')
				return False
		output = False
		for s in self.currentStates:
			if s.isAcceptance:
				output = True
		self.currentStates = {self.initialState} | self.initialState.next_states('&')
		return output
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
		hasEpsilon = False
		for s in self.states:
			for t in s.ndtransitions:
				if t.symbol == '&':
					hasEpsilon = True
		Σ = sorted(self.Σ)
		if hasEpsilon and '&' not in Σ:
			Σ += ['&']
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

	def remove_epsilon_transition(self):
		newStates = set()
		newFinalStates = set()
		for s in self.states:
			#print("s = " + str(s))
			news = copy.deepcopy(s)
			if s == self.initialState:
				newInitial = news
			next_states_by_s = s.next_states('&')
			for symbol in self.Σ:
				trans = copy.deepcopy(news.ndtransitions)
				#print("symbol = " + str(symbol))
				target_states = list()
				for ns in next_states_by_s:
					#print("ns = " + str(ns))
					target_states += ns.next_states(symbol)
				for t in trans:
					#print(trans)
					#print("t = " + str(t))
					#print("target_states = " + str(target_states))
					if t.symbol == '&':
						#print(news.ndtransitions)
						news.ndtransitions = trans[:].remove(t)
					if len(target_states) > 0:
						news.add_transition(NDTransition(symbol, set(target_states)))
			newStates.add(news)
			if news.isAcceptance:
				newFinalStates.add(news)
		return NDAutomaton(newStates, newFinalStates, newInitial, self.Σ)


	'''
		determinization functions:
	'''

	def determinize_states(self, states, finalStates, newStates, determinizedStates):
		if len(states) == 1:
			oldState = list(states)[0]
			newState = State(oldState.name, oldState.isAcceptance)
			if newState in determinizedStates:
				return newState
			determinizedStates.add(newState)
			for t in oldState.ndtransitions:
				newT = Transition(t.symbol, self.determinize_states(t.target_states, finalStates, newStates, determinizedStates))
				newState.add_transition(newT)
				#print(str(newState) + " + " + str(newT))
			if newState in newStates:
				newStates.remove(newState)
			newStates.add(newState)
			if oldState in self.finalStates:
				finalStates.add(newState)
			return newState
		accpt = False
		for s in states:
			accpt = accpt or s.isAcceptance
		newState = State(states.__str__(), accpt)
		if newState in determinizedStates:
			return newState
		determinizedStates.add(newState)
		for a in self.Σ:
			nextStates = set()
			for s in states:
				for t in s.ndtransitions:
					if t.symbol == a:
						nextStates = nextStates | set(t.target_states)
			newState.add_transition(Transition(a, self.determinize_states(nextStates, finalStates, newStates, determinizedStates)))
		if any(s in self.finalStates for s in states):
			finalStates.add(newState)
		if newState in newStates:
			newStates.remove(newState)
		newStates.add(newState)
		return newState

	def determinize(self):
		newA = self.remove_epsilon_transition()
		newStates = set()
		finalStates = set()
		determinized = set()
		for s in newA.states:
			newState = State(s.name, s.isAcceptance)
			newStates.add(newState)
			if s == newA.initialState:
				newInitialState = newState
		for s in newA.finalStates:
			newFinalState = State(s.name, True)
			finalStates.add(newFinalState)
		for s in newA.states:
			newState = State(s.name, s.isAcceptance)
			for t in s.ndtransitions:
				#print(t.target_states)
				#return " "
				newState.add_transition(Transition(t.symbol, newA.determinize_states(t.target_states, finalStates, newStates, determinized)))
			if newState in newStates:
				newStates.remove(newState)
			newStates.add(newState)
		for s in newStates:
			if s == newInitialState:
				newInitialState = s
		for s in newStates:
			for t in s.transitions:
				for os in newStates:
					if t.target_state == os:
						s.remove_transition(t)
						s.add_transition(Transition(t.symbol, os))
		return Automaton(set(newStates), set(finalStates), newInitialState, self.Σ)

class EpsilonAutomaton(NDAutomaton):
	def __init__(self, states, finalStates, initialState, Σ=['0','1']):
		NDAutomaton.__init__(self,states, finalStates, initialState, Σ)

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
