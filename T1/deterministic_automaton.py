from globals import *
import copy


class Automaton:

	def __init__(self, states, finalStates, initialState, Σ=['0','1']):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentState = initialState
		self.Σ = Σ
		self.equi_classes = []
		self.name = None

	def set_name(name):
		self.name = name

	def process_input(self, input):
		for symbol in input:
			self.currentState = self.currentState.next_state(symbol)
			if self.currentState is None:
				return False
			#print(self.currentState)
		return self.currentState.isAcceptance

	def next_state(self, symbol):
		self.currentState = self.currentState.next_state(symbol)
		return self.currentState

	def __str__(self):
		stringerson = "   δ"
		Σ = sorted(self.Σ) + ['&']
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

		for s in copy.deepcopy(test_states):
			if not self.has_path(self.initialState, s) and not(s.name == 'φ'):
				self.states.remove(s)
				self.remove_transitions_from(s)
		self.equi_classes = [set(self.get_acceptance_states()), set(self.get_non_acceptance_states())]

	def remove_transitions_from(self, st):
		for state in self.states:
			for t in state.transitions:
				if t.target_state == st:
					t.target_state = φ(self.Σ)


	def remove_dead_states(self):
		#print("AWQUI: " + str(set(self.states) - set(self.finalStates)))
		for s in set(self.states) - set(self.finalStates):
			if s.name == 'φ':
				continue
			sremove = True
			for fs in self.finalStates:
				if self.has_path(s, fs):
					sremove = False
					#print("existe caminho entre " + str(s) + " " + str(fs))
				#else:
					#print("não existe caminho entre " + str(s) + " " + str(fs))
			if sremove:
				try:
					self.states.remove(s)
					self.remove_transitions_from(s)

				except ValueError:
					pass
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
			#print(str(s.transitions[0]))
			if s.next_state(symbol):
				ret.append(s.next_state(symbol))

		return ret

	def depth_first_search(self, s):

		visited = set()
		stack = [s]

		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				#print(vertex)
				visited.add(vertex)
				#print("alcança: " + str(self.next_states_all(vertex)))
				stack.extend((self.next_states_all(vertex)))

		return visited
	def minimize(self):
		#print(self.get_eq_class(self.initialState))
		#print(self.equi_classes)
		#self.remove_dead_states()
		#self.remove_unreacheable_states()
		#self.remove_dead_states()
		#self.remove_unreacheable_states()
		self.complete()
		changed = True
		while(changed):
			#print(len(self.equi_classes))
			changed = False
			curr_equi_classes = self.equi_classes
			for eqclass in curr_equi_classes:
				#print(curr_equi_classes)
				if self.test_eqclass1(eqclass):
					changed = True

		newStates = set()
		newFinalStates = set()
		newInitialState = State(self.get_eq_class(self.initialState))
		#print(self.equi_classes)
		for eq in self.equi_classes:
			freerealestate = next(iter(eq))
			news = State(str(self.get_eq_class(freerealestate)), freerealestate.isAcceptance)
			if freerealestate.isAcceptance:
				newFinalStates.add(news)
			if freerealestate == self.initialState:
				newInitialState = news
			newStates.add(news)
			'''
			for symbol in self.Σ:
				ns = State(self.get_eq_class(s.next_state(symbol)))
				#newStates.add(ns)
				t = Transition(symbol, ns)
				#print(t)
				news.add_transition(t)
			'''
			'''
				only one state and its transitions of the equivalence class is
				needed. So break for and look for next class
			'''
		print(self.equi_classes)
		for s in newStates:
			for eq in self.equi_classes:
				freerealestate = next(iter(eq))
				for symbol in self.Σ:
					for ns in newStates:
						if ns == State(str(self.get_eq_class(freerealestate.next_state(symbol)))):
							t = Transition(symbol, ns)
							if (s == State(str(eq))):
								s.add_transition(t)
		'''
		for s in newStates:
			print("NOME: " + s.name)

			for symbol in self.Σ:
				ns = State(str(self.get_eq_class(s.next_state(symbol))))
				#newStates.add(ns)
				t = Transition(symbol, ns)
				print(t)
				news.add_transition(t)
		'''
		a = Automaton(newStates, newFinalStates, newInitialState, self.Σ)
		'''for ns in a.states:
			print("TRANSIÇÃO 1: " + str(ns) + " + " + str(ns.transitions[0]))
			print("TRANSIÇÃO 2: " + str(ns) + " + " + str(ns.transitions[1]))
			print("TRANSIÇÃO 3: " + str(ns) + " + " + str(ns.transitions[2]))'''
		#print("batata: " + str(a.depth_first_search(next(iter(newStates)))))
		#print(self.Σ)
		a.remove_dead_states()
		a.remove_unreacheable_states()
		a.equi_classes = [a.get_acceptance_states(), a.get_non_acceptance_states()]

		return a
	'''
		returns the equivalence class of a given state
	'''
	def get_eq_class(self, s):
		for eq in self.equi_classes:
			if s in eq:
				return str(eq)
	def test_eqclass(self, eqclass):
		garbage = set()
		changed = False
		for state in eqclass:
			test_states = eqclass - {state}
			for ts in test_states:
				for symbol in self.Σ:
					n1 = state.next_state(symbol)
					n2 = ts.next_state(symbol)
					if not self.belong_same_equi_class(n1, n2):
						added = False
						for eq in self.equi_classes:
							if eq == eqclass:
								continue
							if self.belong_equi_class(ts, eq):
								eq.add(ts)
								added = True
						if not added:
							self.equi_classes.append({ts})
						self.equi_classes.remove(eqclass)
						eqclass = eqclass - {ts}
						self.equi_classes.append(eqclass)

						#print("testando equivalencia de " + str(state) + \
						#" com " + str(ts) + " pelo simbolo " + symbol + \
						#" e eles nao vao p/ a msm classe " + str(n1) + " " + \
						#str(n2))
						#print(self.equi_classes)
						changed = True
					#else:
						#print("testando equivalencia de " + str(state) + \
						#" com " + str(ts) + " pelo simbolo " + symbol)
		return changed
	def test_eqclass1(self, eqclass):
		garbage = set()
		changed = False
		giulios = set()
		eqclass_temp = eqclass
		s = next(iter(eqclass))

		test_states = eqclass_temp - {s}

		for ts in test_states:
			for symbol in self.Σ:
				n1 = s.next_state(symbol)
				n2 = ts.next_state(symbol)
				#print("testando equivalencia de " + str(s) + \
					#" com " + str(ts) + " pelo simbolo " + symbol + \
					#" e eles vão p/ " + str(n1) + " " + \
					#	str(n2))
				if not self.belong_same_equi_class(n1,n2):
					eqclass_temp = eqclass_temp - {ts}
					giulios.add(ts)
					changed = True
					break
		if changed:
			self.equi_classes.remove(eqclass)
			self.equi_classes.append(eqclass_temp)
			self.equi_classes.append(giulios)

		return changed
	def belong_equi_class(self, ts, eq):
		for s in eq:
			if not (s.isAcceptance == ts.isAcceptance):
				return False
			belong = True
			for symbol in self.Σ:
				if not (self.belong_same_equi_class(s.next_state(symbol),\
					ts.next_state(symbol))):
					belong = False
			if(belong):
				return True
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
			hashable = 'lambda'
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
		State.__init__(self, 'φ')
		for symbol in Σ:
			t = Transition(symbol, self)
			self.transitions.append(t)
	def next_state(self, symbol):
		return self
