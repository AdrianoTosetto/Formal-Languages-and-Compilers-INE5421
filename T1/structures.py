from globals import *
from itertools import cycle
from non_deterministic_automaton import *
from deterministic_automaton import *
UP = 0
DOWN = 1

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
'''
	this function is equivalent to the post order traversal. E.g if you had a binary tree of your regex and used
	the post order algorithm, it would output the same thing that this function outputs. Given the output of this
	function, it is easier to build the expression tree
'''

def polish_notation(infixexpr):
    prec = {}
    prec["("] = 1
    prec["|"] = 2
    prec["."] = 3
    prec["?"] = 4
    prec["*"] = 4
    prec["+"] = 4
    prec["^"] = 5
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    print(" ".join(postfixList))
    return " ".join(postfixList)


class Tree:

	def __init__(self, root_node=None):
		self.root = root_node
		self.symbol = 'a'

	def is_operand(self, char):
		return char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or char in "0123456789"
	def is_operator(self, char):
		return char == '*' or char == '|' or char == "." or char == "?"
	def one_operand_operator(self, char):
		return char == '*' or char == "?"
	def build(self, expr):
		stack = Stack()
		for symbol in expr:
			if symbol == " ":
				continue
			if self.is_operand(symbol):
				n = Node(symbol)
				n.symbol = symbol
				stack.push(n)
			if self.is_operator(symbol):
				if self.one_operand_operator(symbol):
					t1 = stack.pop()
					n  = Node(symbol)
					n.symbol = symbol
					n.left = t1
					stack.push(n)
				else:
					t1 = stack.pop()
					t2 = stack.pop()
					n  = Node(symbol)
					n.symbol = symbol
					n.left = t2
					n.right = t1
					stack.push(n)
		self.root = stack.pop()
		self.root.enumerate()
		return self.root
	def most_left_node(self):
		return self.root.most_left_node()

	def costura(self):
		self.root.costura()


class Pendency:
	def __init__(self, node, action):
		self.node = node
		self.action = action

	def get_pendency(self):
		return (self.node, self.action)

class Node:

	def __init__(self, symbol, left=None, right=None):
		self.left = left
		self.right = right
		self.symbol = symbol
		self.label = -1
		self.traversal = []
		self.costura_node = None
		self.isThreaded = False
	def set_left(self, left):
		self.left = left
	def set_right(self, right):
		self.right = right
	def __str__(self):
		return str(self.label) + " " + self.symbol
	def __repr__(self):
		return self.__str__()
	def most_left_node(self):
		if self.left is None:
			return self
		else:
			return self.left.most_left_node()
	def enumerate(self):
		leaves = (self.get_leaf_nodes())
		#print("leaves: " + str(self.get_leaf_nodes()))
		i = 1
		for leaf in leaves:
			leaf.label = i
			i+=1


	def in_order(self):
		if self.left is not None:
			self.traversal.extend(self.left.in_order())
		
		self.traversal.append(self)
		if self.right is not None:
			self.traversal.extend(self.right.in_order())
		
		ret = self.traversal
		self.traversal = []
		return (ret)

	def costura(self):
		in_order_nodes = self.in_order()
		print(in_order_nodes)
		iter_ = iter(in_order_nodes)
		next(iter_)
		n = None
		for node in in_order_nodes:
			try:
				n = next(iter_)
			except:
				print(str(node.symbol), end="")
				print(" costura para lambda")
				node.costura_node = Node('λ')
				return
			if node.symbol == "." or node.symbol == "|":
				continue
			print(str(node.symbol) + " costura para ", end="")
			print(n.symbol)
			node.costura_node = n
		self.isThreaded = True

	def handle_leaf(self):
		if not self.is_leaf():
			return set()
		node_composition = set()
		if self.costura_node.symbol == ".":
			node_composition |= (self.handle_concatenation(self.costura_node, UP))
		if self.costura_node.symbol == "?":
			node_composition |= (self.handle_optional(self.costura_node, UP))
		if self.costura_node.symbol == "*":
			node_composition |= self.handle_star(self.costura_node, DOWN)
			node_composition |= (self.handle_star(self.costura_node, UP))
		if self.costura_node.symbol == "|":
			node_composition = self.handle_union(self.costura_node, UP)

		return node_composition

	def handle_optional(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		print("visitando o nodo " + str(node))
		node_composition = set()
		pendencies = Stack()
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition |= {node.left}
			if node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN)
			if node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN)
				node_composition |= node.handle_star(node.left, UP)
			if node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN)
				node_composition |= node.handle_optional(node.left, UP)
			if node.left.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN)
		if action == UP:
			visited_up.add(node)
			if node.costura_node.symbol == 'λ':
				node_composition |= {node.costura_node}
				print("deveria parar aqui")
			if node.costura_node.symbol == "*":
				node_composition |= node.handle_star(node.costura_node, DOWN, visited)
				node_composition |= node.handle_star(node.costura_node, UP, visited)
				#pendencies.push(Pendency(node.costura_node, UP))
			if node.costura_node.symbol == ".":
				node_composition |= node.handle_concatenation(node.costura_node, UP, visited_down, visited_up)
			if node.costura_node.symbol == "?":
				node_composition |= node.handle_optional(node.costura_node, UP, visited)
			if node.costura_node.symbol == "|":
				node_composition |= node.handle_union(node.left, DOWN)
		while not pendencies.isEmpty():
			p = pendencies.pop()
			print("kek")
			if p.action == UP:
				if p.node.costura_node.symbol == ".":
					print("antes: " + str(node_composition))
					node_composition |= p.node.handle_concatenation(p.node.costura_node, UP, visited)
					print("dps: " + str(node_composition))
				if p.node.costura_node.symbol == "*":
					print("antes: " + str(node_composition))
					node_composition |= p.node.handle_star(p.node.costura_node, UP, visited)
					print("dps: " + str(node_composition))
			if p.action == DOWN:
				if p.node.right.symbol == "*":
					node_composition |= p.node.handle_star(p.node.left, DOWN, visited)
					node_composition |= p.node.handle_star(p.node.left, UP, visited)
				if p.node.symbol == ".":
					node_composition |= p.node.handle_concatenation(p.node.left, DOWN, visited)

		return node_composition
	def handle_concatenation(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		node_composition = set()
		pendencies = Stack()
		if action == UP:
			visited_up.add(node)
			if node.right.is_leaf():
				node_composition.add(node.right)
			elif node.right.symbol == "*":
				node_composition |= node.handle_star(node.right, DOWN, visited_down, visited_up)
				print("pendencia com " + str(node.right) + " por cima")
				node_composition |= node.handle_star(node.right, UP,  visited_down, visited_up)
			elif node.right.symbol == ".":
				node_composition |= node.handle_star(node.right, DOWN,  visited_down, visited_up)
			elif node.right.symbol == "?":
				node_composition |= node.handle_optional(node.right, DOWN,  visited_down, visited_up)
				node_composition |= node.handle_optional(node.right, UP,  visited_down, visited_up)
				#pendencies.push(Pendency(node.right, UP))
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition.add(node.left)
			elif node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN, visited_down,visited_up)
			elif node.left.symbol == "*":
				node_composition |=  node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |=  node.handle_star(node.left, UP, visited_down, visited_up)
				#pendencies.push(Pendency(node.left), UP)
			elif node.left.symbol == "?":
				node_composition |=  node.handle_optional(node.left, DOWN)
				node_composition |=  node.handle_optional(node.left, UP)
				#pendencies.push(Pendency(node.left), UP)

		while not pendencies.isEmpty():
			p = pendencies.pop()

			if p.action == UP:
				if p.node.costura_node.symbol == ".":
					print("antes: " + str(node_composition))
					node_composition |= p.node.handle_concatenation(p.node.costura_node, UP,  visited_down, visited_up)
					print("dps: " + str(node_composition))
				if p.node.costura_node.symbol == "*":
					print("antes: " + str(node_composition))
					node_composition |= p.node.handle_star(p.node.costura_node, UP,  visited_down, visited_up)
					node_composition |= p.node.handle_star(p.node.costura_node, DOWN,  visited_down, visited_up)
					print("dps: " + str(node_composition))
				if p.node.costura_node.symbol == "?":
					node_composition |= p.node.handle_optional(p.node.costura_node, UP,  visited_down, visited_up)
			if p.action == DOWN:
				if p.node.symbol == ".":
					node_composition |= p.node.handle_concatenation(p.node.costura_node, UP, visited_down, visited_up)
				#if p.node.symbol == 


		return node_composition
	def handle_star(self, node, action, visited_down=set(), visited_up=set()):
		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		pendencies = Stack()
		node_composition = set()
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition.add(node.left)
			elif node.left.symbol == ".":
				node_composition |= node.handle_concatenation(node.left, DOWN,  visited_down, visited_up)
			elif node.left.symbol == "?":
				node_composition |= node.handle_optional(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_optional(node.left, UP,visited_down, visited_up)
				#pendencies.push(node.left, UP)
			elif node.left.symbol == "*":
				node_composition |= node.handle_star(node.left, DOWN, visited_down, visited_up)
				node_composition |= node.handle_star(node.left, UP,  visited_down, visited_up)
		if action == UP:
			visited_up.add(node)
			if node.costura_node.symbol == 'λ':
				node_composition |= {node.costura_node}
			if node.costura_node.symbol == ".":
				node_composition |= node.handle_concatenation(node.costura_node, UP)
			elif node.costura_node.symbol == "?":
				node_composition |= node.handle_optional(node.costura_node, UP,  visited_down, visited_up)
				#pendencies.push(node.left, UP)
			elif node.costura_node.symbol == "*":
				node_composition |= node.handle_star(node.costura_node, DOWN,visited_down, visited_up)
				node_composition |= node.handle_star(node.costura_node, UP,  visited_down, visited_up)
			elif node.costura_node.symbol == "|":
				node_composition |= node.handle_union(node.costura_node, UP, visited_down, visited_up)
		return node_composition
	def handle_union(self, node, action, visited_down=set(), visited_up=set()):

		if node in visited_down and action == DOWN:
			return set()
		if node in visited_up and action == UP:
			return set()
		node_composition = set()
		if action == UP:
			visited_up.add(node)
			right_most = node.right_most_node()
			print("right most "+str(right_most))
			if right_most.costura_node.symbol == "*":
				node_composition |= right_most.handle_star(right_most.costura_node, DOWN)
				node_composition |= right_most.handle_star(right_most.costura_node, UP)
			elif right_most.costura_node.symbol == ".":
				node_composition |= right_most.handle_concatenation(right_most.costura_node, UP)
			elif right_most.costura_node.symbol == "?":
				#node_composition |= right_most.handle_optional(right_most.costura_node, DOWN)
				node_composition |= right_most.handle_optional(right_most.costura_node, UP,visited_down,\
				 visited_up)
			elif right_most.costura_node.symbol == "λ":
				node_composition |= {right_most.costura_node}				
		if action == DOWN:
			visited_down.add(node)
			if node.left.is_leaf():
				node_composition |= {node.left}
			if node.right.is_leaf():
				node_composition |= {node.right}
		return node_composition
	def post_order(self):

		if self.left is not None:
			self.traversal.append(self.left.post_order())
		if self.right is not None:
			self.traversal.append(self.right.post_order())
		traversal.append(self.symbol)
		ret = self.traversal
		self.traversal = []
		return (ret)
	def pre_order(self):
		traversal.append(self.symbol)
		if self.left is not None:
			self.traversal.append(self.left.post_order())
		if self.right is not None:
			self.traversal.append(self.right.post_order())
		ret = self.traversal
		self.traversal = []
		return (ret)
	def get_leaf_nodes(self):
		if self.is_leaf():
			self.traversal.append(self)
		if self.left is not None:
			self.traversal.extend(self.left.get_leaf_nodes())
		if self.right is not None:
			self.traversal.extend(self.right.get_leaf_nodes())
		ret = self.traversal
		self.traversal = []
		return (ret)
	def is_leaf(self):
		return self.right is None and self.left is None

	def right_most_node(self):
		if self.right is not None:
			return self.right.right_most_node()
		else:
			return self
	def handle_root(self):
		visited_up = set()
		visited_down = set()
		node_composition = set()
		if self.symbol == '|':
			if self.right.is_leaf():
				node_composition |= {self.left}
			if self.right.symbol == '*':
				node_composition |= self.handle_star(self.right, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.right, UP, visited_down ,visited_up)
			if self.right.symbol == "|":
				node_composition |= self.handle_star(self.right, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.right, UP, visited_down ,visited_up)
			if self.right.symbol == "?":	
				node_composition |= self.handle_optional(self.right,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.right,UP, visited_down,visited_up)
			if self.right.symbol == ".":
				node_composition |= self.handle_concatenation(self.right,DOWN, visited_down ,visited_up)

			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "?":	
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
		if self.symbol == ".":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "?":	
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)
		
		if self.symbol == "*":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "?":	
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)

			if self.costura_node is not None:
				node_composition |= {self.costura_node}

		if self.symbol == "?":
			if self.left.is_leaf():
				node_composition |= {self.left}
			if self.left.symbol == '*':
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "|":
				node_composition |= self.handle_star(self.left, DOWN, visited_down, visited_up)
				node_composition |= self.handle_star(self.left, UP, visited_down ,visited_up)
			if self.left.symbol == "?":	
				node_composition |= self.handle_optional(self.left,DOWN,visited_down, visited_up)
				node_composition |= self.handle_optional(self.left,UP, visited_down,visited_up)
			if self.left.symbol == ".":
				node_composition |= self.handle_concatenation(self.left,DOWN, visited_down ,visited_up)

			if self.costura_node is not None:
				node_composition |= {self.costura_node}

		return node_composition
class RegExp:
	def __init__(self, regex):
		self.regex = regex
	def get_compositions_from(self,compositions, symbol):
		for c in compositions:
			print(c)
	def to_automaton(self):
		t = Tree()
		nodo = t.build(polish_notation(self.regex))
		t.costura()
		display(nodo, 1)
		leaves = nodo.get_leaf_nodes()
		states_counter = 0
		compositions = {}
		states_compositions = {}
		states = set()
		print("what = " + str(nodo.handle_root()))
		for leaf in leaves:
			compositions[leaf] = leaf.handle_leaf()
		q0 = State('q' + str(states_counter))
		states_compositions[q0] = nodo.handle_root()
		states.add(q0)
		print(compositions)
		self.get_compositions_from(compositions, 'A')
		#print(states_compositions)


def display(root, level):
	if root is None:
		for i in range(0, level):
			print("\t", end="")
		print("=")
		return
	display(root.right, level+1)

	for i in range(0, level):
		print("\t", end="")
	if root.is_leaf():
		print(str(root.label) + root.symbol)
	else:
		print(root.symbol)
	display(root.left, level+1)
