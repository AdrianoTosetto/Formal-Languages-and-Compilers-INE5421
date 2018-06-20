import sys
sys.path.append('../')

import unittest
from read_tests_files import ReadTestsFiles

class CFGTests(unittest.TestCase):

    def build_grammars(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        
    def test_epsilon(self):
        g1 = ReadTestsFiles.read_file_and_get_grammar("g1.txt")
        self.assertEqual(g1.derives_epsilon('S'), True)
        self.assertEqual(g1.derives_epsilon('A'), False)
if __name__ == '__main__':
    unittest.main()