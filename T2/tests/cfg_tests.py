import sys
sys.path.append('../')

import unittest
from read_tests_files import ReadTestsFiles

class CFGTests(unittest.TestCase):

    def build_grammars(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        
    def test_epsilon(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        g2 = ReadTestsFiles.read_file_and_get_grammar("g2.txt")
        self.assertEqual(g1.derives_epsilon('S'), True)
        self.assertEqual(g1.derives_epsilon('A'), False)
        self.assertEqual(g2.derives_epsilon('P'), True)
        self.assertEqual(g2.derives_epsilon('B'), True)
        self.assertEqual(g2.derives_epsilon('K'), True)
        self.assertEqual(g2.derives_epsilon('V'), True)
        self.assertEqual(g2.derives_epsilon('C'), True)
if __name__ == '__main__':
    unittest.main()