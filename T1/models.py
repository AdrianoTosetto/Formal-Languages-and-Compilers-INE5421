class Automaton:

	def __init__(self, states, finalStates, initialState, transitions):
		self.transitions = set(transitions)
		self.states = set(states)
		self.finalStates = set(finalStates)
		self.initialState = initialState
		self.input = []

	def transition_function(self, current_state, symbol):
		for t in self.transitions:
			if t.state == current_state and t.read_symbol == symbol:
				return t.next_state

		return None


class Transition:
	def __init__(self, target_state, symbol):
		self.target_state = target_state
		self.symbol = symbol

class State:
	def __init__(self, name, t=[]):
		self.name = name
		self.transitions = t

	def __str__(self):
		print(self.name)

	def next_state(self, symbol):
		for t in self.transitions:
			if t.symbol == symbol:
				return t.target_state

	def __eq__(self, other):
		return self.name == other


if __name__ == "__main__":
	input1 = ['a', 'a', 'a']
	input2 = ['a','a']
	q0 = State("q0")
	q1 = State("q1")
	t1 = Transition(q0, 'a', q1)
	t2 = Transition(q1, 'a', q1)
	#for t in trs:
	#	print(t.next(q0, 'a'))
	#a = Automaton(set([q0, q1]), set([q1]), q0, trs)

