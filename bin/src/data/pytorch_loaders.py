import torch
import numpy as np
import multiprocessing as mp
from sklearn.preprocessing import OneHotEncoder
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

import sys
sys.path.append("..")
from src.data.generate_fasta import Fasta


class fastaDataset(Dataset, Fasta):
    """
    This class loads a fasta from a file and creates a pytorch dataset with the sequences being one-hot encoded.
    """

    def __init__(self, path_to_fasta, alphabet='acgt'):
        """
        This function initializes the fastaDataset class. 
        """
        Fasta.__init__(self)
        self.one_hot_encoder = OneHotEncoder(categories=[list(alphabet)])
        self.load_fasta(path_to_fasta)
        self.one_hot_encode_sequences_mp()

    def one_hot_encode_sequences_mp(self):
        """ 
        This function one-hot encodes the given contained in self.sequences using multiprocessing.
        """
        # create a pool of processes
        a_pool = mp.Pool(mp.cpu_count())
        # map the function to the pool
        self.sequences = a_pool.map(self.one_hot_encode_sequence, self.sequences)

    def one_hot_encode_sequence(self, sequence):
        """
        This function one-hot encodes the given sequence.
        """
        sequences_transformer_to_array = self._sequence_to_array(sequence)
        return self.one_hot_encoder.fit_transform(sequences_transformer_to_array).toarray()

    def _sequence_to_array(self, sequence):
        """
        This function transforms the given sequence to an array.
        """
        sequence = sequence.lower()
        sequence_array = np.array(list(sequence))
        return sequence_array.reshape(-1, 1)

    def __len__(self):
        """
        This function returns the length of the dataset.
        """
        return len(self.sequences)

    def __getitem__(self, idx):
        """
        This function returns the item at the given index.
        """
        
        # make sure that sequences are reshaped so that they can be inputed to a Conv1d layer
        sequence = self.sequences[idx].reshape(self.sequences[idx].shape[1], self.sequences[idx].shape[0])
        return sequence, self.tags[idx], self.sequence_names[idx]
    