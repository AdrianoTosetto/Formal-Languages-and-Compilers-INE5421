from globals import *

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
			if not self.has_path(self.initialState, s) and not(s.name == "phi"):
				self.states.remove(s)
				self.remove_transitions_from(s)
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]

	def remove_transitions_from(self, st):
		for state in self.states:
			for t in state.transitions:
				if t.target_state == st:
					t.target_state = φ(self.Σ)


	def remove_dead_states(self):
		for s in set(self.states) - set(self.finalStates):
			sremove = True
			for fs in self.finalStates:
				if self.has_path(s, fs):
					sremove = False
			if sremove:
				try:
					self.states.remove(s)
					self.remove_transitions_from(s)

				except ValueError:
					pass
			sremove = True
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]

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
		self.complete()
		print(self.equi_classes)
		#self.remove_dead_states()
		#self.remove_unreacheable_states()
		changed = True
		while(changed):
			print(self.equi_classes)
			changed = False
			for eqclass in self.equi_classes:
				if self.test_eqclass(eqclass):
					changed = True
					break
		print(self.equi_classes)
	def test_eqclass(self, eqclass):
		for state in eqclass:
			test_states = eqclass - {state}
			for ts in test_states:
				for symbol in self.Σ:
					n1 = state.next_state(symbol)
					n2 = ts.next_state(symbol)
					if not self.belong_same_equi_class(n1, n2):
						self.equi_classes.remove(eqclass)
						eqclass = eqclass - {ts}
						self.equi_classes.append(eqclass)
						self.equi_classes.append({ts})
						print("testando equivalencia de " + str(state) + \
						" com " + str(ts) + " pelo simbolo " + symbol + \
						" e eles nao vao p/ a msm classe " + str(n1) + " " + \
						str(n2))
						print(self.equi_classes)
						return True
					else:
						print("testando equivalencia de " + str(state) + \
						" com " + str(ts) + " pelo simbolo " + symbol)
		return False
	def change_equi_classes(self, eqclass_remove, new_eqclass):
		eqclass_remove = eqclass_remove - {new_eqclass}
		self.equi_classes.append({new_eqclass})
	def complete(self):
		for s in self.states:
			s.complete(self.Σ)
		self.states.append(φ(self.Σ))
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]
	def set_(self):
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]

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
