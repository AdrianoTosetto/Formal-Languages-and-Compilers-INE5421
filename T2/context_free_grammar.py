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
		if type(productions) == set:
			productions = list(productions)
		if len(productions) is 0:
			self.productions = [Production('S','a S')]
			productions = [Production('S','a S')]
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
	def get_terminals(self, productions=None):
		productions = self.productions if productions is None else productions
		terminals = []
		leftsides = sorted(set([prod.leftSide for prod in productions]))
		for prod in leftsides:
			prod = parse_sentential_form(prod)
			for symbol in prod:
				if isTerminalSymbol(symbol):
					terminals.append(symbol)
		return sorted(set(terminals))
	def get_non_terminals(self, productions=None):
		productions = self.productions if productions is None else productions
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
		print("haha")
	def validate_productions(self,productions=None):
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
		if isTerminalSymbol(nt[0]):
			return False
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

	def getFirst(self, sententialForm, visited = None):
		visited = set() if visited is None else visited
		if type(sententialForm) == type(''):
			sententialForm = parse_sentential_form(sententialForm)
		if len(sententialForm) == 0 or sententialForm[0] == '&':
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
						if prod[0] not in visited:
							if isNonTerminalSymbol(prod[0]):
								visited |= {prod[0]}
							firstFromProds |= self.getFirst(prod, visited)
				else:
					if prod[0] not in visited:
						if isNonTerminalSymbol(prod[0]):
							visited |= {prod[0]}
						firstFromProds |= self.getFirst(prod, visited)
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
						if prod[0] not in visited:
							if isNonTerminalSymbol(prod[0]):
								visited |= {prod[0]}
							firstFromProds |= self.getFirst(parse_sentential_form(prod), visited)
					i += 1
					if i >= len(sententialForm):
						FIRST |= firstFromProds
						jump = True
						break
			if not jump:
				FIRST |= firstFromProds
			return FIRST

	'''
		This funtion returns the FOLLOW set of a given non-terminal symbol
	'''
	def getFollow(self, non_terminal, visited = None):
		visited = set() if visited is None else visited
		FOLLOW = set()
		if type(non_terminal) == type([]):
			non_terminal = unparse_sentential_form(non_terminal)
		visited |= {non_terminal}
		if non_terminal == self.initial_symbol:
			FOLLOW.add('$')
		non_terminals = self.get_non_terminals(self.productions)
		#non_terminals.pop(non_terminals.index(non_terminal))
		for nt in non_terminals:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				prod = parse_sentential_form(prod)
				if non_terminal in prod:
					aux_first = self.getFirst(prod[prod.index(non_terminal)+1:len(prod)])
					FOLLOW |= aux_first - {'&'}
					if '&' in aux_first:
						if nt not in visited:
							FOLLOW |= self.getFollow(nt, visited)
		return FOLLOW

	def getFirstNT(self, sententialForm, visited = None, include_self = None):
		include_self = True if include_self is None else include_self
		visited = set() if visited is None else visited
		if type(sententialForm) == type(''):
			sententialForm = parse_sentential_form(sententialForm)
		if len(sententialForm) == 0 or sententialForm[0] == '&':
			return set()
		elif isTerminalSymbol(sententialForm[0]):
			return set()
		else:
			FIRST = set()
			if include_self:
				FIRST |= {sententialForm[0]}
			firstFromBottom = set()
			firstFromProds = set()
			sentence = copy.deepcopy(sententialForm)

			prods = self.prod_dict[sententialForm[0].strip()] #get productions from first symbol of the sentential form, if it's a non-terminal
			firstFromProds = set() #this set holds the FIRST set of the first symbol of the sentential form
			for prod in prods:
				prod = parse_sentential_form(prod.strip())
				'''if prod[0] == sententialForm[0]: #if first symbol is equal to the productor
					if self.derives_epsilon(prod[0]): #consider the production only if & is in FIRST of productor
						prod.pop(0)
						if prod[0] not in visited:
							if isNonTerminalSymbol(prod[0]):
								visited |= {prod[0]}
							firstFromProds |= self.getFirstNT(prod, visited)
				else:'''
				if prod[0] not in visited:
					if isNonTerminalSymbol(prod[0]):
						visited |= {prod[0]}
					firstFromProds |= self.getFirstNT(prod, visited)

			while self.derives_epsilon(sentence[0]):
				sentence.pop(0)
				if len(sentence) < 1:
					break
				if sentence[0] not in visited:
					if isNonTerminalSymbol(sentence[0]):
						visited |= {sentence[0]}
					firstFromBottom |= self.getFirstNT(sentence, visited)

			FIRST |= firstFromProds | firstFromBottom
			return FIRST

	def detect_direct_left_recursion(self, non_terminal):
		if type(non_terminal) == type([]):
			non_terminal = unparse_sentential_form(non_terminal)
		nt_productions = self.prod_dict[non_terminal]
		for prod in nt_productions:
			if parse_sentential_form(prod)[0] == non_terminal:
				return True
		return False

	def detect_direct_left_recursion_for_all(self):
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:
			if self.detect_direct_left_recursion(nt):
				return True
		return False

	def detect_all_left_recursion(self, non_terminal):
		if type(non_terminal) == type([]):
			non_terminal = unparse_sentential_form(non_terminal)
		return non_terminal in self.getFirstNT(non_terminal, include_self = False)

	def detect_all_left_recursion_for_all(self):
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:
			if self.detect_all_left_recursion(nt):
				return True
		return False

	def detect_indirect_left_recursion(self, non_terminal):
		if type(non_terminal) == type([]):
			non_terminal = unparse_sentential_form(non_terminal)
		nt_productions = self.prod_dict[non_terminal]
		for prod in nt_productions:
			prod_first = parse_sentential_form(prod)[0]
			if prod_first != non_terminal:
				if non_terminal in self.getFirstNT(prod_first):
					return True
		return False

	def detect_indirect_left_recursion_for_all(self):
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:
			if self.detect_indirect_left_recursion(nt):
				return True
		return False

	def get_NA(self, nt, visited=None):
		visited = set() if visited is None else visited
		cnt = copy.deepcopy(nt)
		#print(cnt)
		cnt = cnt.strip()
		#print(cnt)
		NA = {cnt}
		visited.add(cnt)
		productions = [self.prod_dict[cnt]][0]
		#print(productions)
		for prod in productions:
			#print("PROD = " + str(prod))
			prod = parse_sentential_form(prod)
			if len(prod) == 1 and isNonTerminalSymbol(prod[0]):
				#print("PROD[0] = " + str(prod))
				prod = unparse_sentential_form(prod)
				if prod[0] not in visited:
					NA |= {prod[0]}
					NA |= self.get_NA(prod[0], visited)
				else:
					continue
		#print("NA = " + str(NA))
		return NA

	def remove_simple_productions(self, rename=None):
		rename = True if rename is None else rename
		copy_productions = copy.deepcopy(self.productions)
		copy_productions = [prod for prod in copy_productions if len(parse_sentential_form(prod.rightSide)) > 1 or isTerminalSymbol(parse_sentential_form(prod.rightSide)[0]) or parse_sentential_form(prod.rightSide)[0] == '&']
		new_prods = set()
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:
			n_nt = self.get_NA(nt)
			for n in n_nt:
				for prod in copy_productions:
					if prod.leftSide in n_nt:
						new_prods.add(Production(nt, prod.rightSide))
		new_prods |= set(copy_productions)
		new_prods = list(new_prods)
		if rename:
			newG = Grammar(new_prods, self.name + " (w/o simple productions)", self.initial_symbol)
		else:
			newG = Grammar(new_prods, self.name, self.initial_symbol)
		return newG

	'''def get_follow(self):
		print("RS")'''

	def nt_is_fertile(self, nt):
		nt = nt.strip()
		prods = self.prod_dict[nt]

	def remove_infertile_symbols(self, rename=None):
		rename = True if rename is None else rename
		non_terminals = self.get_non_terminals(self.productions)
		fertiles = set()
		fertiles_temp = set()
		for nt in non_terminals:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				prod = parse_sentential_form(prod)
				isFertile = True
				for symbol in prod:
					if isNonTerminalSymbol(symbol):
						isFertile = False
						break
				if isFertile:
					fertiles_temp |= {nt}
					break
		while fertiles_temp != fertiles:
			fertiles |= fertiles_temp
			for nt in non_terminals:
				nt_productions = self.prod_dict[nt]
				for prod in nt_productions:
					prod = parse_sentential_form(prod)
					isFertile = True
					for symbol in prod:
						if isNonTerminalSymbol(symbol) and symbol not in fertiles_temp:
							isFertile = False
							break
					if isFertile:
						fertiles_temp |= {nt}
						break
		fertiles |= fertiles_temp
		new_prods = set()
		for nt in fertiles:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				prod = parse_sentential_form(prod)
				isFertile = True
				for symbol in prod:
					if isNonTerminalSymbol(symbol) and symbol not in fertiles:
						isFertile = False
						break
				if isFertile:
					new_prods.add(Production(nt, unparse_sentential_form(prod)))
		if len(new_prods) < 1:
			newInitial = 'S'
		else:
			newInitial = self.initial_symbol
		new_prods = list(new_prods)
		if rename:
			newG = Grammar(new_prods, self.name + " (w/o infertile symbols)", newInitial)
		else:
			newG = Grammar(new_prods, self.name, newInitial)
		return newG

	def remove_unreachable_symbols(self, rename=None):
		rename = True if rename is None else rename
		non_terminals = self.get_non_terminals(self.productions)
		reachable = set()
		reachable_temp = {self.initial_symbol}
		while reachable_temp != reachable:
			reachable_next = reachable_temp - reachable
			reachable |= reachable_temp
			for nt in reachable_next:
				nt_productions = self.prod_dict[nt]
				for prod in nt_productions:
					prod = parse_sentential_form(prod)
					for symbol in prod:
						if isNonTerminalSymbol(symbol):
							reachable_temp |= {symbol}
		new_prods = set()
		for nt in reachable:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				new_prods.add(Production(nt, prod))
		if len(new_prods) < 1:
			newInitial = 'S'
		else:
			newInitial = self.initial_symbol
		new_prods = list(new_prods)
		if rename:
			newG = Grammar(new_prods, self.name + " (w/o unreachable symbols)", newInitial)
		else:
			newG = Grammar(new_prods, self.name, newInitial)
		return newG

	def remove_useless_symbols(self, rename = None):
		rename = True if rename is None else rename
		newG = self.remove_infertile_symbols(False).remove_unreachable_symbols(False)
		if rename:
			newG.name = self.name + " (w/o useless symbols)"
		return newG

	def getNE(self):
		'''NE = set()
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:'''

		return set([nt for nt in self.get_non_terminals(self.productions) if self.derives_epsilon(nt)])

	def make_epsilon_free(self, NE_set=None, rename=None):
		rename = True if rename is None else rename
		NE_set = self.getNE() if NE_set is None else NE_set
		p1 = None
		p2 = None
		newInitial = self.initial_symbol
		if self.initial_symbol in NE_set:
			if len(self.prod_dict[self.initial_symbol]) == 1:
				newG = copy.deepcopy(self)
				newG.name += " (epsilon-free)"
				return self
			#print("KKKKKKKKKKKKKKKKKKKKK")
			i = 0
			while 'S' + str(i) in self.get_non_terminals(self.productions):
				i = i + 1
			new_initial = 'S' + str(i)
			p1 = Production(new_initial, self.initial_symbol)
			p2 = Production(new_initial, '&')
			newInitial = new_initial
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
		fproductions = list(set(productions + new_productions))
		fproductions = [prod for prod in fproductions if prod.rightSide.strip() is not "&"]
		if p1 is not None and p2 is not None:
			fproductions = [p1,p2] + fproductions
		if rename:
			newG = Grammar(fproductions, self.name + " (epsilon-free)")
		else:
			newG = Grammar(fproductions, self.name)
		return newG

	def make_proper(self, rename=None):
		rename = True if rename is None else rename
		newG = self.make_epsilon_free()
		newG = newG.remove_simple_productions()
		newG = newG.remove_useless_symbols()
		if rename:
			newG.name = self.name + " (proper)"
		else:
			newG.name = self.name
		return newG

	def get_NF(self):
		#print("ATENÇÃO")
		non_terminals = self.get_non_terminals(self.productions)
		fertiles = set()
		fertiles_temp = set()
		for nt in non_terminals:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				prod = parse_sentential_form(prod)
				isFertile = True
				for symbol in prod:
					if isNonTerminalSymbol(symbol):
						isFertile = False
						break
				if isFertile:
					fertiles_temp |= {nt}
					break
		while fertiles_temp != fertiles:
			#print("fertiles, yo: " + str(fertiles_temp))
			fertiles |= fertiles_temp
			for nt in non_terminals:
				nt_productions = self.prod_dict[nt]
				for prod in nt_productions:
					prod = parse_sentential_form(prod)
					isFertile = True
					for symbol in prod:
						print(symbol)
						if isNonTerminalSymbol(symbol) and symbol not in fertiles_temp:
							#print(str(symbol) + " kkk")
							isFertile = False
							break
					if isFertile:
						#print("nt = " + nt)
						fertiles_temp |= {nt}
						break
				#print("Fertiles = " + str(fertiles))
				#print("Fertiles Temp = " + str(fertiles_temp))
		fertiles |= fertiles_temp
		NF = set(self.get_non_terminals(self.productions)) - fertiles
		return NF

	def get_VI(self):
		self_wo_unreachables = self.remove_unreachable_symbols()
		alphabet_self = set(self.get_terminals()) | set(self.get_non_terminals())
		alphabet_wo = set(self_wo_unreachables.get_terminals()) | set(self_wo_unreachables.get_non_terminals())
		VI = set(alphabet_self) - set(alphabet_wo)
		return VI

	def isEmpty(self):
		return self.initial_symbol in self.get_NF()

	def reachable_by_NT(self, non_terminal):
		nt_productions = self.prod_dict[non_terminal]
		reachable = set()
		reachable_temp = set()
		for prod in nt_productions:
			prod = parse_sentential_form(prod)
			for symbol in prod:
				if isNonTerminalSymbol(symbol):
					reachable_temp |= {symbol}
		while reachable_temp != reachable:
			reachable_next = reachable_temp - reachable
			reachable |= reachable_temp
			for nt in reachable_next:
				nt_productions = self.prod_dict[nt]
				for prod in nt_productions:
					prod = parse_sentential_form(prod)
					for symbol in prod:
						if isNonTerminalSymbol(symbol):
							reachable_temp |= {symbol}
		return reachable

	def isInfinite(self):
		if self.isEmpty():
			return False
		VI = self.get_VI()
		NF = self.get_NF()
		reachable = set(self.get_non_terminals(self.productions)) - VI
		for nt in reachable:
			nt_productions = self.prod_dict[nt]
			for prod in nt_productions:
				cyclic = False
				productive = False
				prod = parse_sentential_form(prod)
				for symbol in prod:
					if symbol in self.reachable_by_NT(nt):
						cyclic = True
					if isTerminalSymbol(symbol):
						productive = True
					if symbol in NF:
						cyclic = False
						productive = False
						break
				if cyclic and productive:
					return True
		return False

	def isFinite(self):
		return not self.isInfinite()

	'''
		This function removes all left recursions from a proper grammar
	'''
	def remove_left_recursion(self):
		#print(self)
		non_terminals = list(self.get_non_terminals(self.productions))
		non_terminals_temp = []
		new_productions = copy.deepcopy(self.prod_dict)
		for nt in non_terminals:
			repeat = True
			while repeat:
				repeat = False
				print(non_terminals_temp)
				print(new_productions[nt])

				for nt2 in non_terminals_temp:
					nt1_prods = copy.deepcopy(new_productions[nt])
					new_prods_list = list(new_productions[nt])
					for prod in nt1_prods:
						parsed_prod = parse_sentential_form(prod)
						if parsed_prod[0] == nt2:
							repeat = True
							parsed_prod_copy = copy.deepcopy(parsed_prod)
							parsed_prod_copy.pop(0)
							nt2_prods = new_productions[nt2]
							new_prods_list.pop(new_prods_list.index(prod))
							for prod2 in nt2_prods:
								new_prod = prod2 + ' ' + unparse_sentential_form(parsed_prod_copy)
								new_prods_list.append(new_prod)
					new_productions[nt] = set(new_prods_list)
			non_terminals_temp.append(nt)
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
				#print("PRODS = " + str(nt_prods))
				nt_prods_copy = copy.deepcopy(nt_prods)
				for prod in nt_prods:
					parsed_prod = parse_sentential_form(prod)
					#print("parsed_prod: " + str(parsed_prod))
					#print("nt: " + str(nt))
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
		#print("resultado: " + str(newG))
		return newG

	def is_factored(self):
		non_terminals = self.get_non_terminals(self.productions)
		for nt in non_terminals:
			nt_productions = list(self.prod_dict[nt])
			for prod in nt_productions:
				for prod2 in nt_productions[nt_productions.index(prod)+1:len(nt_productions)]:
					if self.getFirst(prod) & self.getFirst(prod2):
						return False
		return True

	'''def get_factor(self, non_terminal):
		nt_productions = self.prod_dict[non_terminal.strip()]
		for prod in nt_productions:
			prod = parse_sentential_form(prod)
			intersections = []
			for prod2 in nt_productions:
				intersection = []
				prod2 = parse_sentential_form(prod2)
				i = 0
				not_epsilon = False
				for in range(0, min(len(prod), len(prod2))):
					if prod[i] == prod[i]:
						intersection.append(prod[i])
						i+=1
					else:
						break
				intersections.append(intersection)


	def factorize(self, steps = 1):
		non_terminals = self.get_non_terminals()
		for nt in non_terminals:
			firsts = []
			nt_productions = self.prod_dict[nt.strip()]
			for prods in nt_productions:
				prods = parse_sentential_form(prods)
				for symbol in prods:'''

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
	if parse_sentential_form(symbol)[0] == '&' or parse_sentential_form(symbol)[0] == '$':
		return False
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
