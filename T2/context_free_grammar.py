'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

'''
	for context-free grammars only
'''

class Grammar:
	def __init__(self, productions, name = None):
		if len(productions) is 0:
			self.productions = {Production('S','aS')}
		else:
			self.productions = self.validate_productions(productions)
		self.name = name


	def __hash__(self):
		hashable = self.name
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __str__(self):
		if len(self.productions) == 0:
			return ""
		stringerson = ""
		leftSides = set()
		first = True
		for prods in self.productions:
			if prods.leftSide != self.productions[0].leftSide:
				leftSides.add(prods.leftSide)
		leftSides = [self.productions[0].leftSide] + sorted(leftSides)
		for lefts in leftSides:
			for prods in self.productions:
				if first and lefts is prods.leftSide:
					stringerson = stringerson + lefts + " -> " + prods.rightSide
					first = False
				elif lefts is prods.leftSide:
					stringerson = stringerson + " | " + prods.rightSide
			stringerson = stringerson + "\n"
			first = True
		return stringerson

	def add_production(self, prod):
		self.productions.append(prod)

	@staticmethod
	def parse_productions(self, str):
		'''
			S ->  Ab  | 
		'''
		print("pintos")
	def validate_productions(self,productions):
		return productions

class Production:
	def __init__(self, leftSide, rightSide):
		self.leftSide = leftSide
		self.rightSide = rightSide

	'''
		This function outputs a production in these formats:
			F -> ( E )
			F -> id
			T -> E T1
			E -> E + T
		in which each terminal or non-terminal symbol is separated by an empty
		space
	'''
	def __str__(self):
		if len(rightSide) < 1:
			return ""
		result_string = self.leftSide + " ->"
		for symbol in self.rightSide:
			result_string += " " + symbol
		return result_string
	'''
		This function functions the same as above, but prints only the right
		side of the production (whithout the ->)
	'''
	def printRightSide(self):
		if len(rightSide) < 1:
			return ""
		firstPass = True
		for symbol in self.rightSide:
			if First:
				result_string += symbol
				firstPass = False
			else:
				result_string += " " + symbol
		return result_string

	def __repr__(self):
		return str(self)
	'''
		This function creates a hash code that equals to the sum of the binary
		value of each character in each symbol from both the left and the right
		sides of the production multiplied by their position in the hashable
		string, which consists in all symbols concatenated
	'''
	def __hash__(self):
		hashable = self.leftSide
		for symbol in self.rightSide:
			hashable += symbol
		sigma = 0
		i = 1
		for c in hashable:
			sigma += ord(c) * i
			i += 1
		return sigma

	'''
		This function defines the == operator for productions as being the
		equality between their hash codes
	'''
	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

'''
	This function checks is the given symbol is a terminal symbol by
	checking whether there is an upper-case letter in it
'''
def isTerminalSymbol(self, symbol):
	isTerminal = True
	for character in symbol:
		if character.isupper():
			isTerminal = False
	return isTerminal
'''
	This function checks is the given symbol is a non-terminal symbol by
	checking if the first character is an upper-case letter and the rest of
	the characters are numbers
'''
def isNonTerminalSymbol(self, symbol):
	isNonTerminal = True
	firstPass = True
	if not symbol[0].isupper():
		isNonTerminal = False
	for character in symbol:
		if firstPass:
			if not symbol.isupper():
				isNonTerminal = False
			firstPass = False
		else:
			if not symbol.isdigit():
				isNonTerminal = False
	return isNonTerminal
