from globals import *

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


class BinaryTree:

	def __init__(self, root_node):
		self.root = root_node

class Node:

	def __init__(self, symbol, left=None, right=None):
		self.left = left
		self.right = right
		self.symbol = symbol
		self.traversal = []
	def set_left(self, left):
		self.left = left
	def set_right(self, right):
		self.right = right
	'''
		this function is equivalent to the polish notation (reversed)
	'''
	def post_order(self):

		if self.left is not None:
			self.left.post_order()
		if self.right is not None:
			self.right.post_order()
		traversal.append(self.symbol)
		return (self.symbol)

def display(root, level):
	if root is None:
		for i in range(0, level):
			print("\t", end="")
		print("=")
		return
	display(root.right, level+1)

	for i in range(0, level):
		print("\t", end="")
	print(root.symbol)
	display(root.left, level+1)
