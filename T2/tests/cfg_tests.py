import sys
sys.path.append('../')

import unittest
from read_tests_files import ReadTestsFiles
from T2.context_free_grammar import *

class CFGTests(unittest.TestCase):

    def build_grammars(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")

    def test_epsilon(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        print(g1)
        g2 = ReadTestsFiles.read_file_and_get_grammar("g2.txt")
        self.assertEqual(g1.derives_epsilon('S'), True)
        self.assertEqual(g1.derives_epsilon('A'), False)
        self.assertEqual(g1.derives_epsilon('B'), False)
        self.assertEqual(g1.derives_epsilon('C'), True)
        self.assertEqual(g1.derives_epsilon('D'), True)
        self.assertEqual(g1.derives_epsilon('X'), True)
        self.assertEqual(g1.derives_epsilon('Y'), True)
        self.assertEqual(g2.derives_epsilon('P'), True)
        self.assertEqual(g2.derives_epsilon('B'), True)
        self.assertEqual(g2.derives_epsilon('K'), True)
        self.assertEqual(g2.derives_epsilon('V'), True)
        self.assertEqual(g2.derives_epsilon('C'), True)

    def test_terminal(self):
        self.assertEqual(isTerminalSymbol('S'), False)
        self.assertEqual(isTerminalSymbol('A'), False)
        self.assertEqual(isTerminalSymbol('B'), False)
        self.assertEqual(isTerminalSymbol('C'), False)
        self.assertEqual(isTerminalSymbol('D'), False)
        self.assertEqual(isTerminalSymbol('X'), False)
        self.assertEqual(isTerminalSymbol('Y'), False)
        self.assertEqual(isTerminalSymbol('a'), True)
        self.assertEqual(isTerminalSymbol('b'), True)
        self.assertEqual(isTerminalSymbol('x'), True)
        self.assertEqual(isTerminalSymbol('y'), True)
        self.assertEqual(isTerminalSymbol('d'), True)
        self.assertEqual(isTerminalSymbol('P'), False)
        self.assertEqual(isTerminalSymbol('K'), False)
        self.assertEqual(isTerminalSymbol('V'), False)
        self.assertEqual(isTerminalSymbol(';'), True)
        self.assertEqual(isTerminalSymbol('c'), True)
        self.assertEqual(isTerminalSymbol('v'), True)
        self.assertEqual(isTerminalSymbol('com'), True)

    def test_non_terminal(self):
        self.assertEqual(not isNonTerminalSymbol('S'), False)
        self.assertEqual(not isNonTerminalSymbol('A'), False)
        self.assertEqual(not isNonTerminalSymbol('B'), False)
        self.assertEqual(not isNonTerminalSymbol('C'), False)
        self.assertEqual(not isNonTerminalSymbol('D'), False)
        self.assertEqual(not isNonTerminalSymbol('X'), False)
        self.assertEqual(not isNonTerminalSymbol('Y'), False)
        self.assertEqual(not isNonTerminalSymbol('a'), True)
        self.assertEqual(not isNonTerminalSymbol('b'), True)
        self.assertEqual(not isNonTerminalSymbol('x'), True)
        self.assertEqual(not isNonTerminalSymbol('y'), True)
        self.assertEqual(not isNonTerminalSymbol('d'), True)
        self.assertEqual(not isNonTerminalSymbol('P'), False)
        self.assertEqual(not isNonTerminalSymbol('K'), False)
        self.assertEqual(not isNonTerminalSymbol('V'), False)
        self.assertEqual(not isNonTerminalSymbol(';'), True)
        self.assertEqual(not isNonTerminalSymbol('c'), True)
        self.assertEqual(not isNonTerminalSymbol('v'), True)
        self.assertEqual(not isNonTerminalSymbol('com'), True)

    def test_first(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("g2.txt")
        self.assertEqual(g1.getFirst(['S']), {'a', 'x', 'y', 'd', '&'})
        self.assertEqual(g1.getFirst(['A']), {'a'})
        self.assertEqual(g1.getFirst(['B']), {'b'})
        self.assertEqual(g1.getFirst(['C']), {'x', 'y', '&'})
        self.assertEqual(g1.getFirst(['D']), {'d', '&'})
        self.assertEqual(g1.getFirst(['X']), {'x', '&'})
        self.assertEqual(g1.getFirst(['Y']), {'y', '&'})
        self.assertEqual(g2.getFirst(['P']), {'c', 'v', 'b', '&', ';', 'com'})
        self.assertEqual(g2.getFirst(['B']), {'c', 'v', 'b', '&', 'com'})
        self.assertEqual(g2.getFirst(['K']), {'c', '&'})
        self.assertEqual(g2.getFirst(['V']), {'v', '&'})
        self.assertEqual(g2.getFirst(['C']), {'b', 'com', '&'})
if __name__ == '__main__':
    unittest.main()
