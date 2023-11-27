"""module for generating foreground and background prior to homer analysis"""

import numpy as np
import torch
import torch.optim as optim
import sys
from abc import ABC
from torch.utils.data import DataLoader

sys.path.append("..")
from src.model.mnn_models import Net, BlockNet
from src.data.generate_fasta import Fasta
from src.data.pytorch_loaders import fastaDataset

class HomerForegroundBackgroundSetup(ABC):
    """
    master class for scanning sequences with a convolution filter
    """

    def __init__(self):
        super().__init__()
        self.positive_hit_fasta = Fasta()
        self.negative_hit_fasta = Fasta()

    def write_fastas(self, path_to_folder):
        """
        writes the positive and negative hit fastas to the given folder

        @param path_to_folder: the path to the folder to write the fastas to

        @return: None
        """
        self.positive_hit_fasta.write_fasta(path_to_folder + "positive_hits.fasta")
        self.negative_hit_fasta.write_fasta(path_to_folder + "negative_hits.fasta")

    
class MnnHomerForegroundBackgroundSetup(ABC):
    """
    class for generating foreground and background prior to homer analysis
    """

    def __init__(self, path_hyper_params, path_params, path_input_fasta, batch_size=1000):
        super().__init__()
        self.sequences = []
        self.names = []
        self.labels = []
        self.input_fasta = Fasta()
        self.input_fasta.load_fasta(path_input_fasta)
        self.input_fasta_dataset = fastaDataset(path_input_fasta)
        self.input_fasta_data_loader = DataLoader(self.input_fasta_dataset, batch_size=1, shuffle=False)

    def scan_sequences(self, x):
        pass