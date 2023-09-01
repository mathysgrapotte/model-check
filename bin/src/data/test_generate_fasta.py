""" module to test generate_fasta.py """
import sys
sys.path.append("..")

from src.data.generate_fasta import Fasta
from src.data.generate_fasta import GenerateFasta
from src.data.generate_fasta import GenerateSingleFixedMotifDataset

import unittest

class TestFasta(unittest.TestCase):
    """ test class for the Fasta class """
    def setUp(self):
        """ sets up the test cases """
        self.fasta = Fasta("test.fasta")

    def test_write_fasta(self):
        """ tests the write_fasta method """
        self.fasta.sequences = ["ACTG", "ACTG"]
        self.fasta.sequence_names = ["seq1", "seq2"]
        self.fasta.tags = [1, 2]
        self.fasta.write_fasta()

    def test_load_fasta(self):
        """ tests the load_fasta method """
        self.fasta.write_fasta()
        self.fasta.load_fasta()
        self.assertEqual(self.fasta.sequences, ["ACTG", "ACTG"])
        self.assertEqual(self.fasta.sequence_names, ["seq1", "seq2"])
        self.assertEqual(self.fasta.tags, [1, 2])

class TestGenerateFasta(unittest.TestCase):
    """ test class for the GenerateFasta class """
    def setUp(self):
        """ sets up the test cases """
        self.fasta = GenerateFasta("test.fasta", 10)
    

if __name__ == '__main__':
    unittest.main()