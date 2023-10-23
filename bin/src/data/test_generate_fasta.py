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
        self.fasta_writer = Fasta()
        self.fasta_loader = Fasta()

    def test_write_load_fasta(self):
        """ tests the load_fasta method and write_fasta method """
        self.fasta_writer.sequences = ["ACTG", "ACTG"]
        self.fasta_writer.sequence_names = ["seq1", "seq2"]
        self.fasta_writer.tags = [1, 2]
        self.fasta_writer.write_fasta("test.fasta")
        self.fasta_loader.load_fasta("test.fasta")
        self.assertEqual(self.fasta_loader.sequences, ["ACTG", "ACTG"])
        self.assertEqual(self.fasta_loader.sequence_names, ["seq1", "seq2"])
        self.assertEqual(self.fasta_loader.tags, [1, 2])

class TestGenerateFasta(unittest.TestCase):
    """ test class for the GenerateFasta class """
    def setUp(self):
        """ sets up the test cases """
        self.fasta = GenerateFasta(10)

    def test_get_motif_from_jaspar(self):
        """ tests the get_motif_from_jaspar method """
        pwm = self.fasta.get_motif_from_jaspar("MA0001.1")
        # check if the pwm is the right size, should be 4,10
        self.assertEqual(pwm.shape, (4, 10))
        
    

if __name__ == '__main__':
    unittest.main()