"""module containing the modular neural network model"""
import torch
from torch import nn
import torch.nn.functional as F

class BlockNet(nn.Module):
    """A single block of the modular neural network"""
    def __init__(self, filter_size, size=101):
        super().__init__()
        self.conv = nn.Conv1d(4, 1, filter_size, bias=False)
        self.dense = nn.Linear(size - (filter_size - 1), 1)

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

    
class Net(nn.Module):
    """The modular neural network"""
    def __init__(self, filter_size, size=101):
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
        self.blocks.append(self.last_block)
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