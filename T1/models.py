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
	input1 = ['a', 'a', 'a']
	input2 = ['a','a']
	q0 = State("q0")
	q1 = State("q1")
	t1 = Transition('a', q1)
	t2 = Transition('a', q0)
	q0.add_transition(t1)
	q1.add_transition(t2)
	a = Automaton([q0, q1],[q1],q0)
	a.process_input('aaaa')