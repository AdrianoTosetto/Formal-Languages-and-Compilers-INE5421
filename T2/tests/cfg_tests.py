import unittest

class CFGTests(unittest.TestCase):
    self.g1 = None


    def build_grammars(self):
        productions = [
            Production('S', 'A B'), Production('S', 'C D'), 
            Production('A', 'a A'), Production('A', 'a'),
            Production('B', 'b B'), Production('B', 'b'),
            Production('C', 'X Y'), 
            Production('D', 'd D'), Production('D', '&'),
            Production('X', 'x X'), Production('X', '&'),
            Production('Y', 'y Y'), Production('Y', '&'),    
        ]
        self.g1 = Grammar(productions)
    def test_epsilon(self,)

if __name__ == '__main__':
    unittest.main()