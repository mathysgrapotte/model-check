"""module containing the modular neural network model"""
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch import nn
from copy import deepcopy
from sys import path 

path.append("..")
from src.utils.sequence_logos import plot_weights


class BlockNet(nn.Module):
    """A single block of the modular neural network"""
    def __init__(self, filter_size, size=101):
        super().__init__()
        self.conv = nn.Conv1d(4, 1, filter_size, bias=False)
        self.dense = nn.Linear(size - (filter_size - 1), 1)
        self.filter_size = filter_size

    def forward(self, x):
        """
        Forward pass of the block
        
        @param x: the input to the block

        @return: the output of the block
        """
        x = self.conv(x)
        x = F.relu(x)
        x = x.reshape(x.shape[0], x.shape[2])
        x = self.dense(x)
        # apply sigmoid to get a probability
        output = torch.sigmoid(x)
        return output
    
    def get_convolution_output(self , x):
        """
        Returns the output of the convolutional layer of the block

        @param x: the input to the block

        @return: the output of the convolutional layer of the block
        """
        x = self.conv(x)
        x = F.relu(x)
        return x
    
    def save_convolution_weight_logo(self, path_to_logo):
        """
        Saves the convolutional weights of the block as a sequence logo

        @param path_to_logo: the path to save the sequence logo to plot

        @return: None
        """
        # get the weights of the convolutional layer
        weights = self.conv.weight.detach().cpu().numpy()

        # plot the weights as a sequence logo
        plot_weights(weights, save=True, path_to_file=path_to_logo + ".png")

    


    
class Net(nn.Module):
    """The modular neural network"""
    def __init__(self, filter_size=2, size=101):
        super().__init__()

        self.last_block = BlockNet(filter_size, size=size)
        self.blocks = nn.ModuleList()
        self.len = 0
        self.linear = nn.Linear(self.len+1, 1)
        self.size = size

    def add_block(self, filter_size):
        """
        Adds a block to the model

        @param filter_size: the size of the filter to be used in the new block

        @return: None
        """
        self.last_block.require_grad = False
        self.blocks.append(deepcopy(self.last_block))
        self.last_block = BlockNet(filter_size, size=self.size)
        self.len = len(self.blocks)
        self.linear = nn.Linear(self.len+1, 1)

    def forward(self, x):
        """
        Forward pass of the model

        @param x: the input to the model

        @return: the output of the model
        """
        hidden = self.last_block(x).view(x.shape[0], 1)
        for i, l in enumerate(self.blocks):
            hidden = torch.cat((hidden, self.blocks[i](x).view(x.shape[0], 1)), dim=1)
        output = self.linear(hidden)
        return output
    
    def get_convolution_output_per_block(self, x, block_id='last'):
        """
        Returns the output of the convolutional layer of a block

        @param x: the input to the model
        @param block_id: the id of the block whose convolutional output we want, if block_id is 'last' then the output of the last block is returned, otherwise the output of the block with the given id is returned

        @return: the output of the convolutional layer of the block
        """
        if block_id == 'last':
            return self.last_block.get_convolution_output(x)
        else:
            # check that blcok_id is not out of range
            assert block_id < len(self.blocks), f"block_id must be less than {len(self.blocks)}"
            return self.blocks[block_id].get_convolution_output(x)
        
    def get_hyper_parameters(self):
        """
        Returns a dictionary containing the hyperparameters of the model

        @return: a dictionary containing the hyperparameters of the model
        """

        # get a list for the filter sizes of the blocks
        filter_sizes = [block.filter_size for block in self.blocks]

        # add the filter size of the last block in the end
        filter_sizes.append(self.last_block.filter_size)

        
        return {'filter_size': filter_sizes, 'size': self.size}
    
    def get_filter_size_for_module(self, module_id):
        """
        Returns the filter size of the given module

        @param module_id: the id of the module whose filter size we want

        @return: the filter size of the given module
        """
        # if the module_id is 'last', return the filter size of the last block
        if module_id == 'last':
            return self.last_block.filter_size
        
        # otherwise, return the filter size of the block with the given id
        else:
            # check that module_id is not out of range
            assert module_id < len(self.blocks), f"module_id must be less than {len(self.blocks)}"
            return self.blocks[module_id].filter_size
    
    def build_model(self, hyper_parameters):
        """
        Builds a model from the given hyperparameters

        @param hyper_parameters: the hyperparameters to use to build the model

        @return: None
        """
        # get the filter sizes from the hyperparameters
        filter_sizes = hyper_parameters['filter_size'] 

        # reset the class with the right parameters
        self.__init__(filter_sizes[0], size=hyper_parameters['size'])

        # add the following blocks
        for filter_size in filter_sizes[1:]:
            self.add_block(filter_size)

    def save_convolution_weight_logo_for_block(self, path_to_logo, module_id='last'):
        """
        Saves the convolutional weights of the module as a sequence logo

        @param path_to_logo: the path to save the sequence logo to plot
        @param module_id: the id of the module whose convolutional weights we want to plot

        @return: None
        """
        # if module_id is 'last', plot the convolutional weights of the last block
        if module_id == 'last':
            self.last_block.save_convolution_weight_logo(path_to_logo + "_last")
        
        # otherwise, plot the convolutional weights of the block with the given id
        else:
            # check that module_id is not out of range
            assert module_id < len(self.blocks), f"module_id must be less than {len(self.blocks)}"
            self.blocks[module_id].save_convolution_weight_logo(path_to_logo + "_" + str(module_id))

    def save_all_convolution_weight_logo(self, path_to_logo):
        """
        Saves the convolutional weights of all modules as a sequence logo

        @param path_to_logo: the path to save the sequence logo to plot

        @return: None
        """
        # save the convolutional weights of the last block
        self.save_convolution_weight_logo_for_block(path_to_logo, module_id='last')

        # save the convolutional weights of all blocks
        for i in range(len(self.blocks)):
            self.save_convolution_weight_logo_for_block(path_to_logo, module_id=i)

    def save_all_modules_linear_weights(self, path_to_linear):
        """
        Saves the linear weights of all modules as a sequence logo

        @param path_to_linear: the path to save the sequence logo to plot

        @return: None
        """
        # get the "last_block" dense layer linear weights
        weights = self.last_block.dense.weight.detach().flatten().cpu().numpy()

        # plot the absolute weights as barplot where each bar corresponds to a position, y-scale from 0 to 1 and with the right x-y labels
        plt.bar(range(len(weights)), abs(weights))
        plt.ylim(0, 1)
        plt.xlabel("Position")
        plt.ylabel("Absolute weight")
        plt.title("Last block")
        # xticks every 5th position
        plt.xticks(range(0, len(weights), 5), range(0, len(weights), 5))
        plt.tight_layout()


        # save the plot with dpi
        plt.savefig(path_to_linear + "_linear_last.png", dpi=300)
        plt.close()


        # do the same for all blocks
        for i in range(len(self.blocks)):
            weights = self.blocks[i].dense.weight.detach().flatten().cpu().numpy()
            plt.bar(range(len(weights)), abs(weights))
            plt.ylim(0, 1)
            plt.xlabel("Position")
            plt.ylabel("Absolute weight")
            plt.title("Block " + str(i))
            plt.xticks(range(0, len(weights), 5), range(0, len(weights), 5))
            plt.tight_layout()
            plt.savefig(path_to_linear + "_linear_" + str(i) + ".png", dpi=300)
            plt.close()


