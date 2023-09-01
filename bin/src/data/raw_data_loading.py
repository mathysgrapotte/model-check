import re 
import numpy as np
import os 
import multiprocessing as mp
from math import * 
from Bio import SeqIO 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from abc import ABC, abstractmethod

class FastaLoader(ABC):
    """
    Loads a fasta file
    """

    def __init__(self) -> None:
        pass

    def fasta_parser(self, fasta):
        """
        this functions parses the fasta file

        :param fasta, start, end, return_errors:
        :return seq,label, names : seq is the one hot encoded sequence, label is the mean_tag count of such sequence:
        """

        name = []
        seq = []
        tag = []
        error_sequences = []
        parser_fa = SeqIO.parse(fasta, "fasta")
        a_pool = mp.Pool(mp.cpu_count())
        a = a_pool.map(self.parse_iteration_fasta, parser_fa)

        for i in range(len(a)):
            try:
                seq.append(a[i][0])
                name.append(a[i][1])
                tag.append(a[i][2])
            except TypeError:
                error_sequences.append(i)

        print("There are ", len(error_sequences), " corrupted sequences")
        self.sequences = seq
        self.names = name 
        self.tags = tag

    def one_hot_encode_sequence(self, sequence):
        sequences_transformer_to_array = self._sequence_to_array(sequence)
        one_hot_encoder = OneHotEncoder(categories=[list(self.alphabet)])
        return one_hot_encoder.fit_transform(sequences_transformer_to_array).toarray()

    def _sequence_to_array(self, sequence):
        sequence = sequence.lower()
        sequence_array = np.array(list(sequence))
        return sequence_array.reshape(-1, 1)
    
    def save_all_to_numpy_array(self, path_to_folder):
        path_to_names = path_to_folder + "all_names.npy"
        path_to_sequences = path_to_folder + "all_sequences.npy"
        path_to_tags = path_to_folder + "all_tags.npy"

        np.save(path_to_names, self.names)
        np.save(path_to_sequences, self.sequences)
        np.save(path_to_tags, self.tags)
    
    @abstractmethod
    def parse_iteration_fasta(self, record):
        return NotImplemented
    
class DnaNameTagFastaLoader(FastaLoader):
    """
    Loads a fasta file containing DNA sequences

    """

    def __init__(self, start=None, end=None) -> None:
        self.alphabet = "acgt"
        self.start = start
        self.end = end

    def parse_iteration_fasta(self, record):
        if (record.seq.count('N') == 0) and (record.seq.count('n') == 0):
            header = record.description
            header_splited = header.split('|')
            if (self.start is None) or (self.end is None):
                sequence = str(record.seq)
            else:
                sequence = str(record.seq)[self.start:self.end]

            sequence = self.one_hot_encode_sequence(sequence)
            name = header_splited[0]
            tag = float(header_splited[1])
            return sequence, name, tag 