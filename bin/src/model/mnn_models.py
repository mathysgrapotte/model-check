"""module containing the modular neural network model"""
import torch
import torch.nn.functional as F
from torch import nn
from copy import deepcopy


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
        output = self.dense(x)
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


