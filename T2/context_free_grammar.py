import copy
from globals import *

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

'''
	for context-free grammars only
'''

class Grammar:
	def __init__(self, productions, name = None, initial_symbol = None):
		if len(productions) is 0:
			self.productions = [Production('S','aS')]
		else:
			self.productions = self.validate_productions(productions)
		if name == None:
			i = 1
			newName = "G" + str(i)
			while Grammar([], newName) in Globals.grammars:
				i+=1
				newName = "G" + str(i)
			self.name = newName
		else:
			self.name = name
		self.nts = self.get_non_terminals(productions)
		self.prod_dict = self.get_prod_dict(productions)
		if initial_symbol == None:
			self.initial_symbol = self.productions[0].leftSide
		else:
			self.initial_symbol = initial_symbol
		print(self.prod_dict)

	def get_prod_dict(self, productions):
		ret = {}
		for nt in self.nts:
			dict_value = set()
			for prod in productions:
				if nt == prod.leftSide:
					dict_value.add(prod.rightSide)
			dict_value = set(sorted(dict_value))
			ret[nt] = dict_value
		return ret
	def get_non_terminals(self, productions):
		return sorted(set([prod.leftSide for prod in productions]))
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
					stringerson = stringerson + lefts + " -> " + unparse_sentential_form(parse_sentential_form(prods.rightSide))
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
	'''
		returns if a given nt derives & directly
		at this moment, it is just a helper method
	'''
	def derives_epsilon_directly(self, nt):
		nt = nt.strip()
		prods = self.prod_dict[nt]

		return '&' in prods or '' in prods
	def derives_epsilon(self, nt, visited=None):
		visited = set() if visited is None else visited
		prods = self.prod_dict[nt]
		visited |= set([nt])
		if self.derives_epsilon_directly(nt):
			return True

		for prod in prods:
			if self.produces_some_terminal(prod):
				continue
			if self.produces_epsilon(prod):
				return True
			explode = parse_sentential_form(prod)#prod.split(" ")
			for vn in explode:
				if isNonTerminalSymbol(vn):
					if vn not in visited:
						if self.derives_epsilon(vn, visited):
							return True
		return False

	def get_non_terminals_derive_epsilon(self):
		print("l")

	def produces_some_terminal(self, prod):
		explode = parse_sentential_form(prod)#prod.split(" ")
		for symbol in explode:
			if isTerminalSymbol(symbol):
				return True
		return False
	def produces_epsilon(self, prod):
		explode = parse_sentential_form(prod)#prod.split(" ")
		for nt in explode:
			if not self.derives_epsilon_directly(nt):
				return False
		return True

	'''
		This funtion returns the FIRST set of a given sentential form
	'''

	def getFirst(self, sententialForm):
		if type(sententialForm) == type(''):
			sententialForm = parse_sentential_form(sententialForm)
		if sententialForm[0] == '&' or len(sententialForm) == 0:
			return {'&'}
		elif isTerminalSymbol(sententialForm[0]):
			return {sententialForm[0].strip()}
		else:
			prods = self.prod_dict[sententialForm[0].strip()] #get productions from first symbol of the sentential form, if it's a non-terminal
			firstFromProds = set() #this set holds the FIRST set of the first symbol of the sentential form
			for prod in prods:
				prod = parse_sentential_form(prod.strip())
				if prod[0] == sententialForm[0]: #if first symbol is equal to the productor
					if self.derives_epsilon(prod[0]): #consider the production only if & is in FIRST of productor
						prod.pop(0)
						firstFromProds |= self.getFirst(prod)
				else:
					firstFromProds |= self.getFirst(prod)
			i = 1
			FIRST = set()
			if i >= len(sententialForm):
				FIRST |= firstFromProds
				return FIRST
			jump = False #this variable exists only because Python doesn't have a goto statement; way to go, Python
			while '&' in firstFromProds:
				FIRST |= firstFromProds - {'&'}
				if isTerminalSymbol(sententialForm[i]):
					FIRST |= {sententialForm[i].strip()}
					jump = True
					break
				else:
					prods = self.prod_dict[sententialForm[i].strip()]
					firstFromProds = set()
					for prod in prods:
						firstFromProds |= self.getFirst(parse_sentential_form(prod))
					i += 1
					if i >= len(sententialForm):
						FIRST |= firstFromProds
						jump = True
						break
			if not jump:
				FIRST |= firstFromProds
			return FIRST
	def get_NA(self, nt, visited=None):
		visited = set() if visited is None else visited
		cnt = [nt][0]
		cnt = cnt.strip()
		NA = set(cnt)
		visited.add(cnt)
		productions = [self.prod_dict[cnt]][0]
		for prod in productions:
			if len(prod) == 1 and prod.isupper():
				if prod not in visited:
					NA |= {prod}
					NA |= self.get_NA(prod, visited)
				else:
					continue
		return NA

	def get_follow(self):
		print("RS")
	def nt_is_fertile(self, nt):
		nt = nt.strip()
		prods = self.prod_dict[nt]


	def make_epsilon_free(self, NE_set):
		productions = [self.productions][0]
		new_productions = []
		for prod in productions:
			non_terminals_temp = set([temp for temp in prod.rightSide.split(" ") if isNonTerminalSymbol(temp)])
			#print(str(prod.rightSide) + " " + str(non_terminals_temp))
			non_terminals_temp = non_terminals_temp.intersection(NE_set)
			if non_terminals_temp == set():
				continue
			#print("prod = " + prod.rightSide + " " + str(non_terminals_temp))
			power_set = set(powerset(non_terminals_temp)) - {()}
			#print(power_set)
			for _set in power_set:
				new_prod = [prod.rightSide][0]
				for epsilon_terminal in _set:
					new_prod = new_prod.replace(epsilon_terminal, "")
				new_prod = new_prod.strip()
				import re
				new_prod = re.sub(' +',' ',new_prod)
				if new_prod is not "":
					new_productions.append(Production(prod.leftSide, new_prod))

		#print(Grammar(new_productions))
		print(Grammar(productions + new_productions, self.name + "_epsilon_free"))
	'''
		This function removes all left recursions from a proper grammar
	'''
	def remove_left_recursion(self):
		print(self)
		non_terminals = self.get_non_terminals(self.productions)
		non_terminals_temp = []
		new_productions = copy.deepcopy(self.prod_dict)
		for nt in non_terminals:
			for nt2 in non_terminals_temp:
				nt1_prods = new_productions[nt]
				for prod in nt1_prods:
					parsed_prod = parse_sentential_form(prod)
					if parsed_prod[0] == nt2:
						parsed_prod_copy = copy.deep_copy(parsed_prod)
						parsed_prod_copy.pop(0)
						nt2_prods = new_productions[nt2]
						new_productions[nt].pop(new_productions[nt].index(prod))
						for prod2 in nt2_prods:
							new_prod = prod2 + ' ' + unparse_sentential_form(parsed_prod_copy)
							new_productions[nt].append(new_prod)
			#Removes direct left recursions:
			nt_prods = list(new_productions[nt])
			new_nt = self.rename_non_terminal(nt)
			new_nt_prods = []
			has_direct_left_recursion = False
			for prod in nt_prods:
				parsed_prod = parse_sentential_form(prod)
				if parsed_prod[0] == nt:
					has_direct_left_recursion = True
					break
			if has_direct_left_recursion:
				print("PRODS = " + str(nt_prods))
				nt_prods_copy = copy.deepcopy(nt_prods)
				for prod in nt_prods:
					parsed_prod = parse_sentential_form(prod)
					print("parsed_prod: " + str(parsed_prod))
					print("nt: " + str(nt))
					if parsed_prod[0] != nt:
						nt_prods_copy.pop(nt_prods_copy.index(prod))
						parsed_prod.append(new_nt)
						unparsed_prod = unparse_sentential_form(parsed_prod)
						nt_prods_copy.append(unparsed_prod)
					else:
						parsed_prod.pop(0)
						parsed_prod.append(new_nt)
						unparsed_prod = unparse_sentential_form(parsed_prod)
						new_nt_prods.append(unparsed_prod)
						nt_prods_copy.pop(nt_prods_copy.index(prod))
				new_productions[nt] = set(nt_prods_copy)
				new_productions[new_nt] = set(new_nt_prods) | {'&'}
		new_productions_list = []
		for prods in new_productions[self.initial_symbol]:
			new_productions_list.append(Production(self.initial_symbol, prods))
		for key in new_productions.keys():
			if key != self.initial_symbol:
				for prods in new_productions[key]:
					new_productions_list.append(Production(key, prods))
		newG = Grammar(new_productions_list, self.name + " (w/o left recursions)")
		print("resultado: " + str(newG))
		return newG

	'''
		This function creates a new non-terminal symbol A1 for a given
		non-terminal symbol A. If A1 already exists, A2 is created, and so on.
	'''
	def rename_non_terminal(self, non_terminal):
		non_terminals = self.get_non_terminals(self.productions)
		i = 1
		new_non_terminal = non_terminal + str(i)
		while new_non_terminal in non_terminals:
			i += 1
			new_non_terminal = non_terminal + str(i)
		return new_non_terminal


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
		if len(self.rightSide) < 1:
			return ""
		result_string = self.leftSide + " -> " + unparse_sentential_form(parse_sentential_form(self.rightSide))
		return result_string
	'''
		This function functions the same as above, but prints only the right
		side of the production (whithout the ->)
	'''
	def printRightSide(self):
		if len(self.rightSide) < 1:
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
	def has_simple_production(self):
		return isNonTerminalSymbol(self.rightSide) or " " not in self.rightSide

'''
	This function checks is the given symbol is a terminal symbol by
	checking whether there is an upper-case letter in it
'''
def isTerminalSymbol(symbol):
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
def isNonTerminalSymbol(symbol):
	if symbol is None or symbol == "" or symbol == " " or " " in symbol:
		return False
	if not symbol[0].isupper():
		return False
	for character in symbol[1:(len(symbol))]:
		if not character.isdigit():
			return False
	return True

'''
	This function returns a sentential form as a list of symbols
'''
def parse_sentential_form(sententialForm):
	symbols = [] #the list to be returned
	symbol = '' #an individual symbol to add to the list
	for character in sententialForm:
		if character != ' ':
			symbol += character
		elif len(symbol) > 0:
			symbols.append(symbol)
			symbol = ""
	if len(symbol) > 0:
		symbols.append(symbol)
	return symbols

'''
	This function returns a list of symbols as a sentential form
'''
def unparse_sentential_form(symbols):
	sententialForm = ''
	first = True
	for symbol in symbols:
		if not first:
			sententialForm += ' '
			sententialForm += symbol
		else:
			sententialForm += symbol
			first = False
	return sententialForm

def get_non_terminals_from_production(prod):
	ret = set()
	import re
	prod = re.sub(' +',' ',prod)
	explode = prod.split()

	for e in explode:
		e = e.strip()
		if isNonTerminalSymbol(e):
			ret.add(e)
	return ret

def powerset(iterable):
	from itertools import chain, combinations
	"list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
