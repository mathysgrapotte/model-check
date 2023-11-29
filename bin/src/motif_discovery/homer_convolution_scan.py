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

    def write_fastas(self, path_to_folder, extention=".fasta"):
        """
        writes the positive and negative hit fastas to the given folder

        @param path_to_folder: the path to the folder to write the fastas to

        @return: None
        """
        self.positive_hit_fasta.write_fasta_without_tags(path_to_folder + "positive_hits_" + extention)
        self.negative_hit_fasta.write_fasta_without_tags(path_to_folder + "negative_hits_" + extention)

    
class MnnHomerForegroundBackgroundSetup(HomerForegroundBackgroundSetup):
    """
    class for generating foreground and background prior to homer analysis
    """

    def __init__(self, path_hyper_params, path_params, path_input_fasta):
        super().__init__()
        self.sequences = []
        self.names = []
        self.labels = []
        self.input_fasta = Fasta()
        self.input_fasta.load_fasta(path_input_fasta)
        self.input_fasta_dataset = fastaDataset(path_input_fasta)
        self.input_fasta_data_loader = DataLoader(self.input_fasta_dataset, batch_size=1, shuffle=False)
        self.model = Net()
        self.model.build_model(path_hyper_params)
        self.model.load_state_dict(torch.load(path_params))

    def scan_sequences(self, module_id='last'):
        """
        For the selected module (last if it's the last module, otherwise should be an int).
        Then, at each position, if the output is positive, extract the sequences from the input fasta corresponding to the range [starting position, starting position + filter size]
        Store that sequence in the positive hit fasta, with a label corresponding to the sequence name.
        Do the same for the negative hits

        @return: None
        """

        # setting device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # setting model to eval mode
        self.model.eval()

        # get the filter size for the given module
        filter_size = self.model.get_filter_size_for_module(module_id)

        # for each sequence in the input fasta
        for batch_idx, (data, target, name) in enumerate(self.input_fasta_data_loader):
            # check that the sequence in the data loader and the input fasta have the same name
            assert name[0] == self.input_fasta.sequence_names[batch_idx], f"the sequence names in the data loader and the input fasta are not the same: {name[0]} != {self.input_fasta.sequence_names[batch_idx]}"

            # send data to device
            data, target = data.to(device), target.to(device)

            # convert data and target to float
            data = data.float()

            # forward
            output = self.model.get_convolution_output_per_block(data, module_id)

            # squeeze and detach output
            output = output.squeeze().detach().cpu().numpy()

            # for each position in the output
            for i in range(len(output)):

                
                # get the sequence from the input fasta
                sequence = self.input_fasta.sequences[batch_idx][i:i+filter_size]
                name_sequence = name[0] + "_" + str(i) + "_" + str(i+filter_size)

                # if the output is positive
                if output[i] > 0:
                    # add the sequence to the positive hit fasta
                    self.positive_hit_fasta.sequences.append(sequence)
                    self.positive_hit_fasta.sequence_names.append(name_sequence)
                else:
                    # add the sequence to the negative hit fasta
                    self.negative_hit_fasta.sequences.append(sequence)
                    self.negative_hit_fasta.sequence_names.append(name_sequence)

    def scan_for_all_modules_and_save(self, path_to_folder):
        """
        For each module, scan the sequences and save the positive and negative hits to the given folder

        @param path_to_folder: the path to the folder to save the positive and negative hits to

        @return: None
        """
        # for the first module
        self.scan_sequences('last')

        # write the fastas
        self.write_fastas(path_to_folder, "module_last.fasta")

        # reset the fastas
        self.positive_hit_fasta = Fasta()
        self.negative_hit_fasta = Fasta()
        

        # for each module
        for i in range(len(self.model.blocks)):
            # scan the sequences
            self.scan_sequences(i)

            # write the fastas
            self.write_fastas(path_to_folder, "module_" + str(i) + ".fasta")

            # reset the fastas
            self.positive_hit_fasta = Fasta()
            self.negative_hit_fasta = Fasta()