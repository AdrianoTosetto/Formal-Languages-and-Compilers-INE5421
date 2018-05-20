from globals import *
from itertools import cycle
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
				return
			if node.symbol == "." or node.symbol == "|":
				continue
			print(str(node.symbol) + " costura para ", end="")
			print(n.symbol)
			node.costura_node = n
		self.isThreaded = True

	def node_composition(node):
		# nodo para quem o param node costura
		thread_node = node.costura_node
		if costura_node.symbol == ".":
			print()
	'''
		this function is equivalent to the polish notation (reversed)
	'''

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
