import sys
sys.path.append('../')

import unittest
from read_tests_files import ReadTestsFiles
from context_free_grammar import *

class CFGTests(unittest.TestCase):

    def build_grammars(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")

    def test_epsilon(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        print(g1)
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")
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
        self.assertEqual(g4.derives_epsilon('C'), False)
        self.assertEqual(g4.derives_epsilon('V'), False)

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
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")

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

        self.assertEqual(g4.getFirst(['C']), {'com'})
        self.assertEqual(g4.getFirst(['V']), {'id'})

    def test_follow(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")

        self.assertEqual(g1.getFollow(['S']), {'$'})
        self.assertEqual(g1.getFollow(['A']), {'b'})
        self.assertEqual(g1.getFollow(['B']), {'b', '$'})
        self.assertEqual(g1.getFollow(['C']), {'d', '$'})
        self.assertEqual(g1.getFollow(['D']), {'$'})
        self.assertEqual(g1.getFollow(['X']), {'y', 'd', '$'})
        self.assertEqual(g1.getFollow(['Y']), {'d', '$'})

        self.assertEqual(g2.getFollow(['P']), {'$', ';'})
        self.assertEqual(g2.getFollow(['B']), {'$', ';'})
        self.assertEqual(g2.getFollow(['K']), {'v', 'b', 'com', '$', ';'})
        self.assertEqual(g2.getFollow(['V']), {'b', 'com', '$', ';'})
        self.assertEqual(g2.getFollow(['C']), {'$', 'com', 'e', ';'})

        self.assertEqual(g4.getFollow(['C']), {'$', ';'})
        self.assertEqual(g4.getFollow(['V']), {':='})

    def test_first_nt(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")

        self.assertEqual(g1.getFirstNT(['S']), {'S', 'A', 'C', 'X', 'Y', 'D'})
        self.assertEqual(g1.getFirstNT(['A']), {'A'})
        self.assertEqual(g1.getFirstNT(['B']), {'B'})
        self.assertEqual(g1.getFirstNT(['C']), {'C', 'X', 'Y'})
        self.assertEqual(g1.getFirstNT(['D']), {'D'})
        self.assertEqual(g1.getFirstNT(['X']), {'X'})
        self.assertEqual(g1.getFirstNT(['Y']), {'Y'})

        self.assertEqual(g2.getFirstNT(['P']), {'P', 'B', 'K', 'V', 'C'})
        self.assertEqual(g2.getFirstNT(['B']), {'B', 'K', 'V', 'C'})
        self.assertEqual(g2.getFirstNT(['K']), {'K'})
        self.assertEqual(g2.getFirstNT(['V']), {'V'})
        self.assertEqual(g2.getFirstNT(['C']), {'C'})

        self.assertEqual(g4.getFirstNT(['C']), {'C'})
        self.assertEqual(g4.getFirstNT(['V']), {'V'})

    def test_has_left_recursion(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")
        g8 = ReadTestsFiles.read_file_and_get_grammar("../g8.txt")



        self.assertEqual(g1.detect_direct_left_recursion(['S']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['A']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['B']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['C']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['D']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['X']), False)
        self.assertEqual(g1.detect_direct_left_recursion(['Y']), False)

        self.assertEqual(g1.detect_all_left_recursion(['S']), False)
        self.assertEqual(g1.detect_all_left_recursion(['A']), False)
        self.assertEqual(g1.detect_all_left_recursion(['B']), False)
        self.assertEqual(g1.detect_all_left_recursion(['C']), False)
        self.assertEqual(g1.detect_all_left_recursion(['D']), False)
        self.assertEqual(g1.detect_all_left_recursion(['X']), False)
        self.assertEqual(g1.detect_all_left_recursion(['Y']), False)

        self.assertEqual(g1.detect_indirect_left_recursion(['S']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['A']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['B']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['C']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['D']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['X']), False)
        self.assertEqual(g1.detect_indirect_left_recursion(['Y']), False)



        self.assertEqual(g2.detect_direct_left_recursion(['P']), True)
        self.assertEqual(g2.detect_direct_left_recursion(['B']), False)
        self.assertEqual(g2.detect_direct_left_recursion(['K']), False)
        self.assertEqual(g2.detect_direct_left_recursion(['V']), False)
        self.assertEqual(g2.detect_direct_left_recursion(['C']), True)

        self.assertEqual(g2.detect_all_left_recursion(['P']), True)
        self.assertEqual(g2.detect_all_left_recursion(['B']), False)
        self.assertEqual(g2.detect_all_left_recursion(['K']), False)
        self.assertEqual(g2.detect_all_left_recursion(['V']), False)
        self.assertEqual(g2.detect_all_left_recursion(['C']), True)

        self.assertEqual(g2.detect_indirect_left_recursion(['P']), False)
        self.assertEqual(g2.detect_indirect_left_recursion(['B']), False)
        self.assertEqual(g2.detect_indirect_left_recursion(['K']), False)
        self.assertEqual(g2.detect_indirect_left_recursion(['V']), False)
        self.assertEqual(g2.detect_indirect_left_recursion(['C']), False)



        self.assertEqual(g4.detect_direct_left_recursion(['C']), True)
        self.assertEqual(g4.detect_direct_left_recursion(['V']), False)

        self.assertEqual(g4.detect_all_left_recursion(['C']), True)
        self.assertEqual(g4.detect_all_left_recursion(['V']), False)

        self.assertEqual(g4.detect_indirect_left_recursion(['C']), False)
        self.assertEqual(g4.detect_indirect_left_recursion(['V']), False)



        self.assertEqual(g8.detect_direct_left_recursion(['S']), False)
        self.assertEqual(g8.detect_direct_left_recursion(['B']), False)
        self.assertEqual(g8.detect_direct_left_recursion(['D']), False)
        self.assertEqual(g8.detect_direct_left_recursion(['E']), False)
        self.assertEqual(g8.detect_direct_left_recursion(['F']), False)

        self.assertEqual(g8.detect_all_left_recursion(['S']), False)
        self.assertEqual(g8.detect_all_left_recursion(['B']), True)
        self.assertEqual(g8.detect_all_left_recursion(['D']), True)
        self.assertEqual(g8.detect_all_left_recursion(['E']), True)
        self.assertEqual(g8.detect_all_left_recursion(['F']), True)

        self.assertEqual(g8.detect_indirect_left_recursion(['S']), False)
        self.assertEqual(g8.detect_indirect_left_recursion(['B']), True)
        self.assertEqual(g8.detect_indirect_left_recursion(['D']), True)
        self.assertEqual(g8.detect_indirect_left_recursion(['E']), True)
        self.assertEqual(g8.detect_indirect_left_recursion(['F']), True)

    def test_left_recursion(self):
        print("kkkkkkkkkkkkkkkkkkkkkk")
        '''g1 = ReadTestsFiles.read_file_and_get_grammar("../g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("../g2.txt")
        g4 = ReadTestsFiles.read_file_and_get_grammar("../g4.txt")
        g8 = ReadTestsFiles.read_file_and_get_grammar("../g8.txt")

        self.assertEqual(g1.remove_left_recursion().detect_all_left_recursion_for_all(), False)
        self.assertEqual(g2.remove_left_recursion().detect_all_left_recursion_for_all(), False)
        self.assertEqual(g4.remove_left_recursion().detect_all_left_recursion_for_all(), False)
        self.assertEqual(g8.remove_left_recursion().detect_all_left_recursion_for_all(), False)'''

    def test_simple_productions(self):
        g5 = ReadTestsFiles.read_file_and_get_grammar("../g5.txt")
        g6 = ReadTestsFiles.read_file_and_get_grammar("../g6.txt")
        g7 = ReadTestsFiles.read_file_and_get_grammar("../g7.txt")
        self.assertEqual(g5.get_NA('E'), {'E', 'T', 'F', 'P'})
        self.assertEqual(g5.get_NA('T'), {'T', 'F', 'P'})
        self.assertEqual(g5.get_NA('F'), {'F', 'P'})
        self.assertEqual(g5.get_NA('P'), {'P'})
        self.assertEqual(g6.get_NA('S'), {'S'})
        self.assertEqual(g6.get_NA('B'), {'B', 'E', 'F'})
        self.assertEqual(g6.get_NA('D'), {'D', 'F'})
        self.assertEqual(g6.get_NA('E'), {'E'})
        self.assertEqual(g6.get_NA('F'), {'F'})
        self.assertEqual(g7.get_NA('S'), {'S'})
        self.assertEqual(g7.get_NA('B'), {'B', 'E', 'F', 'D'})
        self.assertEqual(g7.get_NA('D'), {'B', 'E', 'F', 'D'})
        self.assertEqual(g7.get_NA('E'), {'B', 'E', 'F', 'D'})
        self.assertEqual(g7.get_NA('F'), {'B', 'E', 'F', 'D'})
if __name__ == '__main__':
    unittest.main()
