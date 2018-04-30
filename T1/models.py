class Automaton:

	def __init__(self, states, finalStates, initialState):
		self.states = (states)
		self.finalStates = (finalStates)
		self.initialState = initialState
		self.currentState = initialState

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
		ret = "["
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


if __name__ == "__main__":
	'''input1 = ['a', 'a', 'a']
	input2 = ['a','a']
	q0 = State("q0")
	q1 = State("q1")
	t1 = Transition('a', q1)
	t2 = Transition('a', q0)
	q0.add_transition(t1)
	q1.add_transition(t2)
	a = Automaton([q0, q1],[q1],q0)
	a.process_input('aaaa')'''
	q0 = NDState("q0")
	q1 = NDState("q1")
	q2 = NDState("q2")
	t0 = NDTransition('0',[q0, q1])
	t1 = NDTransition('1', [q2])
	t2 = NDTransition('0',[q1, q2])
	q0.add_transition(t0)
	q1.add_transition(t1)
	q1.add_transition(t2)
	a = NDAutomaton([q0,q1], [q2], q0)
	a.transition_table()
	print(a.next_states('0'))
	print(a.next_states('0'))