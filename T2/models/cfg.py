class CFG:
    
    def __init__(self, *rules):
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        temp = rule.split('->')
        return tuple([temp[0], temp[1].split("|")])
        
    def __getitem__(self, nonterminal):
        yield from [rule for rule in self.rules 
                    if rule[0] == nonterminal]
        
    @staticmethod
    def is_nonterminal(symbol):
        return symbol.isalpha() and symbol.isupper()
        
    @property
    def nonterminals(self):
        return set(nt for nt, _ in self.rules)
        
    @property
    def terminals(self):
        return set(
            symbol
            for _, expression in self.rules
            for symbol in expression
            if not self.is_nonterminal(symbol)
        )


if __name__ == "__main__":
    g = CFG(\
    '^->A',
    'AA->BBC|B',
    'A->1',
    'B->C',
    'B->2',
    'C->32',
    'C->1',)
    print(g.rules)
    #print(g.__getitem__('A'))
    #sprint(g.__getitem__('A'))